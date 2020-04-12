import random
import sched
import threading
import time
from Queue import Queue
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

import pytest
import thrift_connector.connection_pool as connection_pool

from src.Constant.constant import constant
from src.initializer.generateThrift import luci
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.utilities.logger import Logger


class Test_MultiInstanceIssueRedeem():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
        constant.config['requestId'] = 'luci_auto_' + str(random.randint(11111, 99999))
        self.coupon_series_id = -1
        self.tillId = constant.config['tillIds'][0]
        self.billId = str(random.randint(11111, 99999))
        self.queue = Queue()
        self.lock = threading.Lock()
        # create connection pool
        port = constant.config['luciPort'].next()
        self.connObj = connection_pool.ClientPool(
            luci.LuciService,
            '127.0.0.1',
            port,
            connection_class=connection_pool.ThriftPyCyClient,
            timeout=150
        )
        self.s = sched.scheduler(time.time, time.sleep)

    def initialize(self):
        self.user_id = []
        for i in xrange(1, self.number_of_runs + 1, 1):
            self.user_id.append(i)
        self.result = {'label': 'default', 'queued_count': self.number_of_runs, 'total_issue_time': 0,
                       'total_issue_count': 0, 'avg_issue_time': 0, 'total_redeem_time': 0, 'total_redeem_count': 0,
                       'avg_redeem_time': 0}

    @pytest.mark.parametrize('description, number_of_runs, number_of_threads, simultaneous_issue_redeem',
                             [('Luci multi thread coupon issue redeem', 1000, 25, False)])
    def test_IC_RC_010_PERF(self, description, number_of_runs, number_of_threads, simultaneous_issue_redeem):
        Logger.log('starting tc execution')
        self.number_of_runs = number_of_runs
        self.issue_pool = ThreadPool(number_of_threads)
        self.redeem_pool = ThreadPool(number_of_threads)
        self.initialize()

        # Save Coupon Config
        coupon_config_obj, self.coupon_series_id = LuciHelper.saveCouponConfigAndAssertions(self)
        time.sleep(2)

        print_stats_thread = threading.Thread(target=self.scheduler, name="print stats thread", args=('print_stats',))
        print_stats_thread.start()

        redeem_thread = threading.Thread(target=self.scheduler, name="redeem coupons thread", args=('redeem_coupons',))
        if simultaneous_issue_redeem:
            redeem_thread.start()

        func = partial(self.issue_coupon, self.coupon_series_id)
        self.issue_pool.map(func, self.user_id)

        if not simultaneous_issue_redeem:
            redeem_thread.start()
        redeem_thread.join()

        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId=self.coupon_series_id, no_issued=self.number_of_runs,
                                               no_redeemed=self.number_of_runs)

        self.print_details()
        Logger.log('All done!!!')

    def scheduler(self, arg):
        if arg == 'print_stats':
            self.s.enter(5, 1, self.print_stats, ())
            self.s.run()
        elif arg == 'redeem_coupons':
            self.s.enter(5, 1, self.redeem_coupon_from_queue, ())
            self.s.run()

    def issue_coupon(self, coupon_series_id, userId):
        with self.lock:
            self.result['queued_count'] -= 1

        issue_coupon_obj = {'couponSeriesId': coupon_series_id, 'storeUnitId': self.tillId, 'userId': userId}
        issue_coupon_request = LuciObject.issueCouponRequest(issue_coupon_obj)
        # Issue coupon request
        start = time.time()
        coupon_details = self.connObj.issueCoupon(issue_coupon_request).__dict__
        end = time.time()
        total = end - start

        with self.lock:
            self.result['total_issue_count'] += 1
            self.result['total_issue_time'] += total
            self.result['avg_issue_time'] = self.result['total_issue_time'] / self.result['total_issue_count']

        self.queue.put((userId, coupon_details['couponCode']))

    def redeem_coupon(self, issued_coupons, isRedeem=True):
        coupon_list = issued_coupons[1]
        if not isinstance(issued_coupons, list):
            coupon_list = [issued_coupons[1]]
        redeem_coupon_request = LuciHelper.redeemCouponRequest(coupon_list, issued_coupons[0],
                                                               redeemCouponRequest={'commit': isRedeem})
        start = time.time()
        self.connObj.redeemCoupons(redeem_coupon_request)
        end = time.time()
        total = end - start
        self.queue.task_done()
        with self.lock:
            self.result['total_redeem_count'] += 1
            self.result['total_redeem_time'] += total
            self.result['avg_redeem_time'] = self.result['total_redeem_time'] / self.result['total_redeem_count']

    def redeem_coupon_from_queue(self):
        while True:
            if (self.result['total_issue_count'] == self.result['total_redeem_count']) or self.queue.empty():
                break
            coupon = self.queue.get()
            self.redeem_pool.map(self.redeem_coupon, [coupon])

    def print_stats(self):
        if (self.result['total_redeem_count'] != self.number_of_runs) and not self.queue.empty():
            self.print_details()
            self.s.enter(1, 1, self.print_stats, ())

    def print_details(self):
        Logger.log("Queued: ", self.result['queued_count'],
                   " Issued count: ", self.result['total_issue_count'],
                   " Total Issued Time: ", self.result['total_issue_time'],
                   " Redeem count: ", self.result['total_redeem_count'],
                   " Total redeemed Time: ", self.result['total_redeem_time'],
                   " Avg Issued time: ", round(self.result['avg_issue_time'] * 1000, 2),
                   " Avg Redeemed time: ", round(self.result['avg_redeem_time'] * 1000, 2))
