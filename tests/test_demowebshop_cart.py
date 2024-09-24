import json

import requests
from allure_commons.types import AttachmentType
from selene import browser, be, have
import logging
from allure import attach, step

base_url = 'https://demowebshop.tricentis.com'


def test_add_product_to_cart():
    with step('Add product to cart (API)'):
        response = requests.post(base_url + '/addproducttocart/catalog/43/1/1')
        attach(body=response.request.url, name='Request', attachment_type=AttachmentType.TEXT,
               extension="txt")
        attach(body=json.dumps(dict(response.request.headers),
                               indent=4, ensure_ascii=True), name='Request Headers',
               attachment_type=AttachmentType.JSON,
               extension="json")
        attach(body=json.dumps(response.json(),
                               indent=4, ensure_ascii=True), name="Response", attachment_type=AttachmentType.JSON,
               extension="json")
        attach(body=str(response.cookies.get('Nop.customer')), name="Cookies", attachment_type=AttachmentType.TEXT,
               extension="txt")
        logging.info(response.request.url)
        logging.info(response.status_code)
        logging.info(response.text)

    with step('Get cookies from API'):
        cookie = response.cookies.get('Nop.customer')

    with step('Set cookies from API'):
        browser.open(base_url + '/cart')
        browser.driver.add_cookie({'name': 'Nop.customer', 'value': cookie})

    with step('Open cart page'):
        browser.open(base_url + '/cart')

    with step('Verify availability of product in cart and its quantity (UI)'):
        browser.element('.cart').element('.product').element('[href="/smartphone"]').should(be.visible)
        browser.element('.qty-input').should(have.attribute('value', '1'))

    with step('Close browser'):
        browser.quit()
