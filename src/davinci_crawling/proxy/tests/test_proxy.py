# -*- coding: utf-8 -*-
# Copyright (c) 2019 BuildGroup Data Services Inc.
import logging
import re
import time

from caravaggio_rest_api.tests import CaravaggioBaseTest
from davinci_crawling.crawler import Crawler
from davinci_crawling.net import fetch_file, fetch_page, DEFAULT_TIMEOUT, get_json
from davinci_crawling.proxy.proxy import ProxyManager
from django.conf import settings


_logger = logging.getLogger("davinci_crawling.testing")

CHROME_OPTIONS = {"chromium_bin_file": settings.CHROMIUM_BIN_FILE}

ProxyManager.set_proxy_manager("davinci_crawling.proxy.proxy_mesh.ProxyMesh")


class TestProxy(CaravaggioBaseTest):
    """
    Test the proxy logic, this test requires connection with internet
    because we use the proxy mesh api and request for real pages.
    """

    all_files_count = 0

    @classmethod
    def setUpTestData(cls):
        pass

    def _get_ip(self, driver):
        """
        Get the current ip using the whatismyip service and a driver.
        Args:
            driver: the chromium driver.

        Returns:
            the ip returned by the service.
        """
        driver.get("https://api.ipify.org/")

        ip = re.search("((?:[0-9]{1,3}.){3}[0-9]{1,3})", driver.page_source)

        if ip is None:
            return None

        return ip.group(1)

    def test_changing_ips_single_proxy(self):
        """
        Test if selenium is changing ips using the proxy, to check that we will
        download the whatismyip.com website and get the ip received.
        """
        web_driver = Crawler.get_web_driver(**CHROME_OPTIONS)

        generated_ips = []
        for _ in range(10):
            ip = self._get_ip(web_driver)

            if not ip:
                continue

            self.assertIsNotNone(ip)

            generated_ips.append(ip)

        # get the ratio of different ips
        ratio = float(len(set(generated_ips))) / len(generated_ips)
        _logger.info("Ratio of new ips: %s", ratio)

        self.assertTrue(ratio > 0.1)

    def test_changing_ips_many_proxies(self):
        """
        Test if selenium is changing ips using the proxy, to check that we will
        download the whatismyip.com website and get the ip received.
        """

        generated_ips = []
        for _ in range(10):
            web_driver = Crawler.get_web_driver(**CHROME_OPTIONS)
            ip = self._get_ip(web_driver)

            generated_ips.append(ip)

        # get the ratio of different ips
        ratio = float(len(set(generated_ips))) / len(generated_ips)
        _logger.info("Ratio of new ips: %s", ratio)

        self.assertTrue(ratio > 0.1)

    def test_download(self):
        """
        Test download file using proxy.
        """
        generated_ips = []
        for _ in range(10):
            file = fetch_file("https://api.ipify.org/?file", {})
            f = open(file.file, "r")
            generated_ips.append(f.readline())

        # get the ratio of different ips
        ratio = float(len(set(generated_ips))) / len(generated_ips)
        _logger.info("Ratio of new ips: %s", ratio)

        self.assertTrue(ratio > 0.1)

    def test_fetch_page(self):
        """
        Test fetch page using proxy.
        """
        generated_ips = []
        for _ in range(10):
            content = fetch_page("https://api.ipify.org/", DEFAULT_TIMEOUT)
            generated_ips.append(content.text)

        # get the ratio of different ips
        ratio = float(len(set(generated_ips))) / len(generated_ips)
        _logger.info("Ratio of new ips: %s", ratio)

        self.assertTrue(ratio > 0.1)

    def test_get_json(self):
        """
        Test get_json using proxy.
        """
        generated_ips = []
        for _ in range(10):
            content = get_json("https://api.ipify.org/")
            generated_ips.append(content.text)

        # get the ratio of different ips
        ratio = float(len(set(generated_ips))) / len(generated_ips)
        _logger.info("Ratio of new ips: %s", ratio)

        self.assertTrue(ratio > 0.1)

    def test_quality_checker(self):
        proxy_manager = ProxyManager()
        worked = False
        for _ in range(5):
            try:
                self.assertNotEquals(proxy_manager.get_available_proxies(), proxy_manager.get_to_use_proxies())
                worked = True
                break
            except AssertionError:
                time.sleep(5)

        self.assertTrue(worked)
