import hashlib
import os
import random


class randValues():
    @staticmethod
    def randomString(size):
        return hashlib.md5(os.urandom(128)).hexdigest()[:int(size)]

    @staticmethod
    def randomInteger(digits):
        return random.randint(10 ** (int(digits) - 1), 10 ** int(digits))

    @staticmethod
    def randomEmailId(differentDomains=False):
        domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com"]
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]
        if differentDomains:
            return 'testAutomation_irisv2_' + str(random.choice(letters)) + str(randValues.randomInteger(5)) + str(
                random.choice(domains))
        else:
            return 'testAutomation_irisv2_' + str(random.choice(letters)) + str(
                randValues.randomInteger(5)) + '@gmail.com'  # + str(random.choice(domains))

    @staticmethod
    def getRandomMobileNumber(append='91'):
        return append + str(random.randint(7000000000, 8999999999))
