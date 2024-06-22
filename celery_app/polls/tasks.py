from celery import shared_task  # type: ignore
import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from bs4 import BeautifulSoup
import datetime
import pandas as pd
import csv
import random
import logging
from selenium.webdriver.common.action_chains import ActionChains, ActionBuilder, PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.keys import Keys
from appiumng.models import Search, Profile, Device, SearchResult
from django.utils import timezone
    
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename=f'log/{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.log',  # ログをファイルに出力する場合
                    filemode='w')  # ファイルを上書きモードで開く ('a' で追記モード)

logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
profile_sum = 0

class WebSearcher:
	def __init__(self) -> None:
		pass
	





def change_airplane_mode(driver):
		driver.terminate_app('com.apple.mobilesafari')

		el1 = driver.find_element(by=AppiumBy.CLASS_NAME, value="XCUIElementTypeSwitch")
		
		value = el1.get_attribute("value")
		logger.info(value)
		if value == "0":
			el1.click()
		else:
			logger.info("機内モードがONのためOFFにします")
			el1.click()
			time.sleep(1)
			el1.click()

		time.sleep(1)
		el2 = driver.find_element(by=AppiumBy.CLASS_NAME, value="XCUIElementTypeSwitch")
		el2.click()



def change_profile(driver, device)->int:
	driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Safari").click()
	
	
	el = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="TabOverviewButton")
	logger.info(el)
	if len(el) > 0:
		el[0].click()
		time.sleep(1)
		el = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="TabOverviewButton")
		time.sleep(1)
		logger.info(el)
	
	logger.info("プロファイルを変更")


	el2 = driver.find_elements(by=AppiumBy.XPATH, value="//XCUIElementTypeButton[@name=\"完了\"]")
	logger.info(len(el2))
	while len(el2) > 0:
		el2[0].click()
		el2 = driver.find_elements(by=AppiumBy.XPATH, value="//XCUIElementTypeButton[@name=\"完了\"]")
		logger.info(len(el2))
		time.sleep(1)
	

	el = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Close")
	logger.info(el)
	if len(el) > 0:
		el[0].click()
		el = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Close")
		logger.info(el)
		time.sleep(1)
	
	for i in range(5):
		el4 = driver.find_elements(by=AppiumBy.IOS_CLASS_CHAIN, value="**/XCUIElementTypeButton[`name == \"Close\"`][" + str(i+1) + "]")
		if len(el4) > 0:
			el4[0].click()
			time.sleep(1)

	time.sleep(1)
	logger.info("再度確認")

	el = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Close")
	logger.info(el)
	if len(el) > 0:
		el[0].click()
		el = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Close")
		logger.info(el)
		time.sleep(1)
	for i in range(5):
		el4 = driver.find_elements(by=AppiumBy.IOS_CLASS_CHAIN, value="**/XCUIElementTypeButton[`name == \"Close\"`][" + str(i+1) + "]")
		if len(el4) > 0:
			el4[0].click()
			time.sleep(1)

	time.sleep(1)
	while True:
		el4 = driver.find_elements(by=AppiumBy.XPATH, value='//XCUIElementTypeOther[@name="favoritesItemIdentifierHeader"]/XCUIElementTypeOther/XCUIElementTypeStaticText')
		if len(el4) > 0:
			break
		logger.info("再度確認")
		el = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Close")
		logger.info(el)
		if len(el) > 0:
			el[0].click()
			el = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Close")
			logger.info(el)
			time.sleep(1)
		for i in range(5):
			el4 = driver.find_elements(by=AppiumBy.IOS_CLASS_CHAIN, value="**/XCUIElementTypeButton[`name == \"Close\"`][" + str(i+1) + "]")
			if len(el4) > 0:
				el4[0].click()
				time.sleep(1)



	now_profile = el4[0].get_attribute("name")
	logger.info(now_profile)
	now_profile = now_profile.split(",")[0]
	now_profile = now_profile.split("-")[0]


	time.sleep(1)
	logger.info(now_profile)
	el3 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="TabOverviewButton")
	el3.click()
	logger.info("プロファイルをクリック")
	now_profile = now_profile.strip()



	time.sleep(1)
	try:
		now_profile = str(int(now_profile))
		logger.info(now_profile)
		logger.info(f"TabGroupsButton?Profile={now_profile}")	
		el5 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=f"TabGroupsButton?Profile={now_profile}")
		el5.click()
	except:
		logger.info("お気に入りの場合")
		now_profile = "個人用"
		logger.info(now_profile)
		el5 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value=f"TabGroupsButton?Profile={now_profile}")
		el2 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="TabGroupsButton?Profile=%E5%80%8B%E4%BA%BA%E7%94%A8")

		if len(el5) > 0:
			el5[0].click()
		elif len(el2) > 0:
			el2[0].click()
		else:
			for i in range(device.profile_num):
				logger.info(i)
				now_profile = str(i + 1)
				el5 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value=f"TabGroupsButton?Profile={now_profile}")
				if len(el5) > 0:
					logger.info(f"TabGroupsButton?Profile={now_profile}")
					el5[0].click()
					break
		
	logger.info(device.profile_num)
		
	if now_profile == "個人用":
		profile = random.randint(1, device.profile_num)
		click_profile = 1
		el7 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="プロファイル")
		el7.click()
		logger.info("click_profile:{}".format(click_profile))
		time.sleep(2)

		el8 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="ProfileSwitcher-{}".format(click_profile))
		el8.click()
	else:
		now_profile = int(now_profile)
		
		#1 ~ 100 の profile をnow_profile の　5 以内 でrandom選択
		profile = random.randint(1, 5) + now_profile
		logger.info(f'profile:{profile}')
		if profile < 1:
			profile = 1
		elif profile > device.profile_num:
			profile = 1
		logger.info(f'profile:{profile}')
		logger.info(f'now_profile:{now_profile}')
		logger.info(f'profile - now_profile:{profile - now_profile}')
		while True:
			logger.info(now_profile - profile)
			diff = profile - now_profile
			logger.info(diff)
			if diff > 6:
				now_profile = now_profile + 5
				click_profile = now_profile
			elif diff < -6:
				now_profile = now_profile - 5
				click_profile = now_profile
			else:
				click_profile = profile
				if now_profile == profile:
					profile = profile + 1
				
				now_profile = profile
				
			logger.info("wait")
			time.sleep(4)
			logger.info("wait")
			el7 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="プロファイル")
			el7.click()
			logger.info("click_profile:{}".format(click_profile))
			time.sleep(2)
			try:
				el8 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="ProfileSwitcher-{}".format(click_profile))
				el8.click()
			
			except:
				click_profile = 1
				el8 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="ProfileSwitcher-{}".format(click_profile))
				el8.click()

			if now_profile != profile:
				logger.info("now_profile != profile")
				el5 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=f"TabGroupsButton?Profile={now_profile}")
				el5.click()
				time.sleep(1)
			else:
				break

	el2 = driver.find_elements(by=AppiumBy.XPATH, value="(//XCUIElementTypeButton[@name=\"Close\"])[1]")
	logger.info(el2)
	while len(el2) > 0:
		el2[0].click()
		el2 = driver.find_elements(by=AppiumBy.XPATH, value="(//XCUIElementTypeButton[@name=\"Close\"])[1]")
		time.sleep(1)
		logger.info(el2)
	
	el = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Close")
	if len(el) > 0:
		el[0].click()

	logger.info("ホームに戻る")
	driver.execute_script('mobile: pressButton', {'name': 'home'})
	time.sleep(1)
	return profile


def change_ua(driver, UA):
	logger.info(driver.context)
	driver.switch_to.context('NATIVE_APP')
	logger.info(driver.context)
	el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Unagent")
	el1.click()
	logger.info("Unagentをクリック")
	el2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="グローバル")
	el2.click()
	logger.info("グローバルをクリック")
	
	time.sleep(1)
	el4 = driver.find_elements(by=AppiumBy.CLASS_NAME, value="XCUIElementTypeTextView")
	logger.info(el4)
	if len(el4) > 0:
		if type(UA) == str and (UA != "0" or UA != ""):
			el4[0].clear()
			el4[0].send_keys(UA)

	driver.execute_script('mobile: pressButton', {'name': 'home'})
	logger.info("ホームに戻る")


def search_data(driver, search_word, UA, profile,latitude, longitude, ip="", device=None):
	
	# context をプリント
	count = 0
	
	while True:
		logger.info(count)
		if count > 5:
			element = driver.find_element(by=AppiumBy.CLASS_NAME, value="HzHK1")
			element.click()
		count += 1
		logger.info("天気を検索")
		if not (latitude == 0 and longitude == 0):
			if count > 5:
				driver.find_element(by=AppiumBy.CLASS_NAME, value="HzHK1")
				
			driver.get("https://www.google.co.jp/search?q=天気")
			time.sleep(2)
			logger.info(driver.contexts)
			time.sleep(2)
			logger.info(driver.contexts)

			time.sleep(2)
			logger.info(driver.contexts)
			time.sleep(1)
			logger.info(driver.contexts)
			if len(driver.contexts) != 3:
				driver.terminate_app('com.apple.mobilesafari')
			
				time.sleep(2)
				logger.info(driver.context)
				driver.switch_to.context('NATIVE_APP')
				logger.info(driver.context)
				time.sleep(2)
				continue
			next_step = False
			for i in range(2):
				logger.info(driver.contexts)
				time.sleep(1)
				logger.info(driver.contexts)
				logger.info(driver.contexts[i+1])
				driver.switch_to.context(driver.contexts[i+1])
				logger.info(driver.context)
				time.sleep(3)

				logger.info("contextを変更")

				time.sleep(1)
				elements = driver.find_elements(by=AppiumBy.CLASS_NAME, value="HzHK1")

				logger.info(elements)



				if len(elements):
					if not (latitude == 0 and longitude == 0):
						el13 = driver.find_element(by=AppiumBy.CLASS_NAME, value="HzHK1")
						el13.click()
					next_step = True
					break
				elements = driver.find_elements(by=AppiumBy.CLASS_NAME, value="pTm6Gf")
				if len(elements):
					if not (latitude == 0 and longitude == 0):
						elements[0].click()
					next_step = True
					break
			
			if next_step == False:
				driver.terminate_app('com.apple.mobilesafari')
				time.sleep(1)
				logger.info(driver.context)
				driver.switch_to.context('NATIVE_APP')
				logger.info(driver.context)

				time.sleep(1)
				continue
		
		if not (latitude == 0 and longitude == 0):
			el2 = driver.find_elements(by=AppiumBy.CLASS_NAME, value="bWHbab")
			logger.info(el2)
			if len(el2):
				el2[0].click()
			break
		else:
			break

	time.sleep(2)
	# 現在の context をプリント
	if not (latitude == 0 and longitude == 0):
		logger.info("正確な現在地を使用をクリックする前")
		time.sleep(1)
		logger.info(driver.context)
		driver.switch_to.context('NATIVE_APP')
		logger.info(driver.context)

		time.sleep(1)
		logger.info("正確な現在地を使用")
		el2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="正確な現在地を使用")
		el2.click()
	time.sleep(1)
	#home に戻る
	logger.info("ホームに戻る")


	driver.execute_script('mobile: pressButton', {'name': 'home'})
	
	time.sleep(1)

	if UA != "no-UA":
		change_ua(driver, UA)
	time.sleep(1)
	logger.info("Safariを開く");


	el3 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Safari")
	el3.click()
	time.sleep(1)

	logger.info(driver.contexts)
	time.sleep(1)
	logger.info(driver.contexts)

	logger.info("検索ボックスに入力")

	driver.switch_to.context(driver.contexts[1])
	logger.info(driver.contexts)


	el3 = driver.find_element(by=AppiumBy.XPATH, value="//div[@id=\"qslc\"]/a/img")
	el3.click()
	time.sleep(1)

	while True:
		logger.info(driver.context)
		driver.switch_to.context('NATIVE_APP')
		logger.info(driver.context)
		time.sleep(1)
		
		el2 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="ログインしない")
		if len(el2) > 0:
			el2[0].click()
		el2 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="利用しない")
		if len(el2) > 0:
			el2[0].click()
		el2 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Stay in Safari")
		if len(el2) > 0:
			el2[0].click()
		time.sleep(1)



		logger.info(driver.contexts)
		time.sleep(1)
		logger.info(driver.contexts)

		driver.switch_to.context(driver.contexts[1])
		logger.info(driver.context)

		logger.info("検索ボックスに入力")
		time.sleep(1)
		
		
		el2 = driver.find_elements(by=AppiumBy.XPATH, value='//*[@name="q"]')
		
		if len(el2) > 0:
			el2[0].send_keys(search_word)
			el2[0].send_keys(Keys.RETURN)

			
		logger.info("検索ボタンをクリック")
		driver.switch_to.context('NATIVE_APP')
		logger.info(driver.context)

		el2 = driver.find_elements(by=AppiumBy.XPATH, value="//XCUIElementTypeOther[@value=\"\n\"]")
		if len(el2) > 0:
			el2[0].click()
			
			el2 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="Search")
			if len(el2) > 0:
				el2[0].click()


		time.sleep(10)
		

		logger.info(driver.contexts)
		time.sleep(1)


		driver.switch_to.context(driver.contexts[1])

		driver.refresh()
		
		logger.info(driver.context)
		time.sleep(3)
	
		logger.info("検索結果を取得(sp)")	
		elements = driver.find_elements(by=AppiumBy.CLASS_NAME, value="MjjYud")

		logger.info("検索結果を取得(pc)")
		elements_pc = driver.find_elements(by=AppiumBy.CSS_SELECTOR, value=".egMi0.kCrYT")

		if len(elements) == 0 < len(elements_pc):
			elements = elements_pc
		#google 検索結果 10件をCSVに保存
		logger.info("検索結果を取得")
		logger.info(elements)
		logger.info(elements_pc)
		
		target_a = None
		target_title = None
		logger.info("output.csvに書き込み")
		with open("data/output.csv", "a") as f:
			out_csv = csv.writer(f)
			logger.info(len(elements))
			break_flg = False
			sub_search_url = None
			for i in range(len(elements)):
				logger.info(i)
				a = elements[i].find_elements(by=AppiumBy.TAG_NAME, value="a")
					
				logger.info(a)
				if len(a) == 0:
					continue

				for k in range(len(a)):
					
					if a[k].get_attribute("href") is None:
						continue
					logger.info(a[k].get_attribute("href"))
					if sub_search_url is None:
						sub_search_url = a[k]
					if a[k].get_attribute("href").split("&url=")[-1].split("?q=")[-1].split("&")[0].startswith('http') == False:
						logger.info(i)
						logger.info("httpから始まっていないのでスキップします")
						logger.info(target_a)
						continue

					if a[k].get_attribute("href").split("&url=")[-1].split("?q=")[-1].split("&")[0].startswith('https://www.google'):
						logger.info(i)
						logger.info("google検索結果なのでスキップします")
						continue
					
					## 小要素にjscontroller="Da4hkd"がある場合はスキップ
					if len(a[k].find_elements(by=AppiumBy.XPATH, value=".//div[@jscontroller=\"Da4hkd\"]")) > 0:
						logger.info("jscontroller=\"Da4hkd\"があるのでスキップします")
						continue
					## 小要素にjsmodel="QPRQHf"がある場合はスキップ
					if len(a[k].find_elements(by=AppiumBy.XPATH, value=".//div[@jsmodel=\"QPRQHf\"]")) > 0:
						logger.info("jsmodel=\"QPRQHf\"があるのでスキップします")
						continue

					logger.info(a[k].get_attribute("href"))
					target_a = a[k].get_attribute("href").split("&url=")[-1].split("?q=")[-1].split("&")[0]

					try:
						a[k].click()
					except:
						continue
					
					logger.info("break")
					break_flg = True
					break
				
				if break_flg:
					break
			if target_a is None:
				target_a = sub_search_url
				
			if target_a is not None:
				logger.info(target_a)
			
				time.sleep(3)
				actions = ActionChains(driver)
				actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
				actions.w3c_actions.pointer_action.move_to_location(176, 499)
				actions.w3c_actions.pointer_action.pointer_down()
				actions.w3c_actions.pointer_action.move_to_location(176, 284)
				actions.w3c_actions.pointer_action.release()
				actions.perform()
				time.sleep(3)
				actions = ActionChains(driver)
				actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
				actions.w3c_actions.pointer_action.move_to_location(176, 284)
				actions.w3c_actions.pointer_action.pointer_down()
				actions.w3c_actions.pointer_action.move_to_location(176, 499)			
				actions.w3c_actions.pointer_action.release()
				actions.perform()
				time.sleep(3)
				target_title = driver.title


				driver.execute_script("window.history.back();")
				time.sleep(3)
				out_csv.writerow([search_word,datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),target_title,target_a,profile,ip,'正しく処理が終了しました'])
				break
			else:
				logger.info("検索結果が取得できませんでした")
				# 1ページ戻る
				driver.back()
				time.sleep(3)

	logger.info(driver.context)
	driver.switch_to.context('NATIVE_APP')
	logger.info(driver.context)
	time.sleep(3)


	el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="TabOverviewButton")
	el1.click()

	
	el2 = driver.find_elements(by=AppiumBy.XPATH, value="(//XCUIElementTypeButton[@name=\"Close\"])[2]")
	while len(el2) > 0:
		el2[0].click()
		el2 = driver.find_elements(by=AppiumBy.XPATH, value="(//XCUIElementTypeButton[@name=\"Close\"])[2]")
		time.sleep(1)
		for i in range(5):
			el4 = driver.find_elements(by=AppiumBy.IOS_CLASS_CHAIN, value="**/XCUIElementTypeButton[`name == \"Close\"`][" + str(i+1) + "]")
			if len(el4) > 0:
				el4[0].click()
				time.sleep(1)



	el3 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Close")
	el3.click()



def work(airplane_mode, latitude, longitude, search_word, profile, UA, device):
	logger.info(f'airplane_mode:{airplane_mode} latitude:{latitude} longitude:{longitude} search_word:{search_word} profile:{profile} UA:{UA}')
	options = AppiumOptions()
	options.load_capabilities({
		"platformName": "iOS",
		"appium:automationName": "XCUITest",
		"appium:includeSafariInWebviews": True,
		"appium:connectHardwareKeyboard": True,
		"startIWDP": True,
		'showXcodeLog': True,
		'udid': device.udid,
	})
	url = "http://host.docker.internal:4444/wd/hub"
	driver = webdriver.Remote(url, options=options)
	try:
		
		driver.implicitly_wait(3)
		time.sleep(1)
		udid = driver.capabilities.get('udid', 'UDID not available')
		logger.info(udid)
		logger.info(device.udid)
	
		driver.terminate_app('com.apple.mobilesafari')
		if airplane_mode:
			change_airplane_mode(driver)
		logger.info("ホームに戻る")
		driver.execute_script('mobile: pressButton', {'name': 'home'})
		

		logger.info("位置情報を設定")
		logger.info(latitude)
		logger.info(longitude)

		if latitude == 0 and longitude == 0:
			logger.info("位置情報を設定しない")
		else:
			driver.set_location(latitude,longitude, 0)
		time.sleep(1)
		
		native_UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1'
		change_ua(driver, native_UA)
		time.sleep(1)
		ip = ""
		count = 0
		while True:
			logger.info(count)
			if count > 5:
				element = driver.find_element(by=AppiumBy.XPATH, value='//*[@id="tmContHeadStr"]/div/div[1]/div[3]/div[1]')
				element.click()
			time.sleep(5)
			driver.get('https://www.cman.jp/network/support/go_access.cgi')
			time.sleep(5)
			logger.info(driver.contexts)
			time.sleep(1)
			logger.info(driver.contexts)
			time.sleep(1)
			logger.info(driver.contexts)
			for i in range(len(driver.contexts)):
				logger.info(driver.contexts[i])

				if i == 0:
					continue
				try:
					driver.switch_to.context(driver.contexts[i])
					time.sleep(1)
					ip = driver.find_element(by=AppiumBy.XPATH, value='//*[@id="tmContHeadStr"]/div/div[1]/div[3]/div[1]').text
				except:
					pass
				if ip == "":
					count += 1
					continue
				else:
					break
			if ip == "":
				driver.terminate_app('com.apple.mobilesafari')
				time.sleep(1)
				logger.info(driver.context)
				driver.switch_to.context('NATIVE_APP')
				logger.info(driver.context)
			else:
				logger.info('ip:')
				logger.info(ip)
				break


		logger.info(driver.context)
		driver.switch_to.context('NATIVE_APP')
		logger.info(driver.context)
		time.sleep(1)
		profile = change_profile(driver, device)

		search_data(driver, search_word, UA, profile, latitude, longitude, ip, device)

		time.sleep(1)
		## safariを止める
		driver.terminate_app('com.apple.mobilesafari')


		logger.info("正常終了")
		
		time.sleep(3)
		driver.quit()
		time.sleep(3)
		logger.info("終了")
		return (True, device, ip)
	except Exception as e:
		logger.error(e)
		driver.quit()
		return (False, device, ip)
			
			
def profile_create(profile, device, delete=False):
	profile_sum = profile.profile_sum
	print(profile_sum)
	url = "http://host.docker.internal:4444/wd/hub"
	options = AppiumOptions()
	options.load_capabilities({
		"platformName": "iOS",
		"appium:automationName": "XCUITest",
		"appium:includeSafariInWebviews": True,
		"appium:connectHardwareKeyboard": True,
		"startIWDP": True,
		"udid": device.udid,
	})
	print(device.udid)


	driver = webdriver.Remote(url, options=options)
	driver.execute_script('mobile: pressButton', {'name': 'home'})
	time.sleep(1)
	driver.terminate_app('com.apple.settings')
	time.sleep(1)
	el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="設定")
	el1.click()
	el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Safari")
	el1.click()
	# delete profile
	if delete:
		for i in range(device.profile_num):
			logger.info(i)
			logger.info("delete")
			el2 = driver.find_elements(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"{i+1}\"]")
			while len(el2) > 0:
				el2[0].click()
				el8 = driver.find_element(by=AppiumBy.XPATH, value="//XCUIElementTypeCell[@name=\"プロファイルを削除\"]")
				el8.click()
				el9 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="削除")
				el9.click()
				time.sleep(1)
				el2 = driver.find_elements(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"{i+1}\"]")
		
		device.profile_num = 0
		device.Profile = profile
		device.save()

	# create profile
 
	for i in range(device.profile_num, profile_sum):
		logger.info(i)
		logger.info("create")

		while True:
			logger.info(i)
			el7 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="新規プロファイル")
			logger.info(el7)
			logger.info("create")

			if len(el7) > 0:
				el7[0].click()
				break
			else :
				actions = ActionChains(driver)
				actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
				actions.w3c_actions.pointer_action.move_to_location(176, 499)
				actions.w3c_actions.pointer_action.pointer_down()
				actions.w3c_actions.pointer_action.move_to_location(176, 284)
				actions.w3c_actions.pointer_action.release()
				actions.perform()


		el3 = driver.find_element(by=AppiumBy.CLASS_NAME, value="XCUIElementTypeTextField")
		el3.send_keys(str(i+1))
		el4 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Return")
		el4.click()
		el5 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="完了")
		el5.click()
		while True:
			logger.info(i)
			el7 = driver.find_elements(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"{i+1}\"]")
			if len(el7) > 0:
				el7[0].click()
				break
			else :
				actions = ActionChains(driver)
				actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
				actions.w3c_actions.pointer_action.move_to_location(176, 499)
				actions.w3c_actions.pointer_action.pointer_down()
				actions.w3c_actions.pointer_action.move_to_location(176, 284)
				actions.w3c_actions.pointer_action.release()
				actions.perform()
			time.sleep(1)
			
		el10 = driver.find_element(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"Unagent\"]")
		el10.click()
		el11 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="checkmark")
		if len(el11) == 0:
			el10 = driver.find_element(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"Unagent\"]")
			el10.click()
		
		el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Safari")
		el1.click()
		device.profile_num = i + 1
		device.save()
	
	driver.quit()

		



@shared_task
def appium() -> None:
	airplane_mode = True
	#Profileの中で一番日付が最新のものを取得
	devices = Device.objects.all()
	for device in devices:
		profile = Profile.objects.filter(Device=device).order_by('-date')[0]
		device_profile = device.Profile
		if device_profile != profile:
			profile_create(profile, device, delete=True)

		elif device.profile_num != profile.profile_sum:
			profile_create(profile, device,	delete=False)

	searchs = Search.objects.all()
	for search_data in searchs:
			# 1日の検索回数を超えている場合はスキップ
			searched = SearchResult.objects.filter(search=search_data, datetime__date=datetime.datetime.now(), success=True)
			logger.info(searched)
			logger.info(search_data.count_by_day)
			if len(searched) >= search_data.count_by_day:
				continue
			logger.info(search_data)
			location = search_data.location
			
			user_agent = search_data.user_agent
			search_result = SearchResult()

			search_result.search = search_data
			search_result.datetime = timezone.now()
			search_result.success = True
			logger.info(device)
			search_result.Device = device
			search_result.save()

			success, device, ip = work(airplane_mode, location.latitude, location.longitude, search_data.search, profile, user_agent.user_agent, search_data.Device)
			
			search_result.datetime = timezone.now()
			search_result.success = success
			search_result.ip = ip
			search_result.save()
			time.sleep(search_data.rest_time)
	