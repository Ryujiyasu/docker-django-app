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
	
options = AppiumOptions()

options.load_capabilities({
	"platformName": "iOS",
	"appium:automationName": "XCUITest",
	"appium:includeSafariInWebviews": True,
	"appium:connectHardwareKeyboard": True,
	"startIWDP": True
})
url = "http://localhost:4444/wd/hub"
# location.tsv を読み込む
location = pd.read_csv("data/location.csv", index_col=0)
# 重複削除
# search.tsv を読み込む
search = pd.read_csv("data/search.csv", index_col=0)



def change_airplane_mode(driver):
	# 機内モードON／OFF
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



def change_profile(driver)->int:
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
			for i in range(profile_sum):
				logger.info(i)
				now_profile = str(i + 1)
				el5 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value=f"TabGroupsButton?Profile={now_profile}")
				if len(el5) > 0:
					logger.info(f"TabGroupsButton?Profile={now_profile}")
					el5[0].click()
					break
		
		
	if now_profile == "個人用":
		profile = random.randint(1, profile_sum)
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
		profile = random.randint(-3, 5) + now_profile
		if profile < 1:
			profile = 1
		elif profile > profile_sum:
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


def search_data(driver, search_word, UA, profile,latitude, longitude, ip=""):
	
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

	change_ua(driver, UA)
	time.sleep(1)


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



def work(airplane_mode, latitude, longitude, search_word, profile, UA):
	
	while True:
		try:

			logger.info(f'airplane_mode:{airplane_mode} latitude:{latitude} longitude:{longitude} search_word:{search_word} profile:{profile} UA:{UA}')
			driver = webdriver.Remote(url, options=options)
			driver.implicitly_wait(3)
			time.sleep(1)

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
			profile = change_profile(driver)

			search_data(driver, search_word, UA, profile, latitude, longitude, ip)

			time.sleep(1)
			## safariを止める
			driver.terminate_app('com.apple.mobilesafari')


			logger.info("正常終了")
			
			time.sleep(3)
			driver.quit()
			time.sleep(3)
			break
			
			

		except Exception as e:
			logger.info(e)
			time.sleep(5)
			try:
				driver.terminate_app('com.apple.mobilesafari')
				elements = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="モバイル通信")
				if len(elements) > 0:
					elements[0].click()
			except:
				pass
			time.sleep(3)

			logger.info("異常終了")
			driver.quit()
			time.sleep(3)

def dummy_work():
	time.sleep(5)
	logger.info("dammy_work")

def profile_create(profile_sum):
	print(profile_sum)
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
	for i in range(200):
		logger.info(i)
		el2 = driver.find_elements(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"{i+1}\"]")
		while len(el2) > 0:
			el2[0].click()
			el8 = driver.find_element(by=AppiumBy.XPATH, value="//XCUIElementTypeCell[@name=\"プロファイルを削除\"]")
			el8.click()
			el9 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="削除")
			el9.click()
			time.sleep(1)
			el2 = driver.find_elements(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"{i+1}\"]")
			
	# create profile
 
	for i in range(profile_sum):
		logger.info(i)
		el2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="新規プロファイル")
		el2.click()
		el3 = driver.find_element(by=AppiumBy.CLASS_NAME, value="XCUIElementTypeTextField")
		el3.send_keys(str(i+1))
		el4 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Return")
		el4.click()
		el5 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="完了")
		el5.click()
		el7 = driver.find_element(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"{i+1}\"]")
		el7.click()
		el10 = driver.find_element(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"Unagent\"]")
		el10.click()
		el11 = driver.find_elements(by=AppiumBy.ACCESSIBILITY_ID, value="checkmark")
		if len(el11) == 0:
			el10 = driver.find_element(by=AppiumBy.XPATH, value=f"//XCUIElementTypeCell[@name=\"Unagent\"]")
			el10.click()
		
		el1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Safari")
		el1.click()
		time.sleep(1)
		



@shared_task
def appium() -> None:
    airplane_mode = True
    no_search_count = 0
    no_search_flg = False
    for i in range(len(search)):
        # location に移動
        start_time_str = search.iloc[i]["検索開始時間"] # 0:00
        end_time_str = search.iloc[i]["検索終了時間"] # 23:59
        now = datetime.datetime.now()
        start_time = datetime.datetime.strptime(start_time_str, '%H:%M')
        start_time = start_time.replace(year=now.year, month=now.month, day=now.day)
        end_time = datetime.datetime.strptime(end_time_str, '%H:%M')
        end_time = end_time.replace(year=now.year, month=now.month, day=now.day)
        now = datetime.datetime.now()
        search = search.fillna("0")
        # dayを知りたい
        logger.info(now.date())

        try:
            if datetime.datetime.now().date() != datetime.datetime.strptime(search.iloc[i]['exec_time'],'%Y/%m/%d %H:%M:%S').date():
                search.iat[i, 7] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                search.iat[i, 8] = 0.0
                search.to_csv("data/search.csv")
                continue
    
        except:
            try:
                if datetime.datetime.now().date() != datetime.datetime.strptime(search.iloc[i]['exec_time'],'%Y/%m/%d %H:%M').date():
                    search.iat[i, 7] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                    search.iat[i, 8] = 0.0
                    search.to_csv("data/search.csv")
                    continue


            except:
                search.iat[i, 7] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
                search.iat[i, 8] = 0.0
                search.to_csv("data/search.csv")
                continue

        today_profile = ''
        
        with open("data/profile.csv", "r") as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if row[0] == datetime.datetime.now().strftime('%Y/%-m/%d') and not (row[2] == "1" or row[2] == "1.0"):
                    today_profile = row[0]
                    profile_sum = int(row[1])
                    break
                elif row[0] == datetime.datetime.now().strftime('%Y/%-m/%d'):
                    today_profile = ''
                    profile_sum = int(row[1])
        print('today_profile')
        print(today_profile)

        if today_profile != '':
            profile_create(profile_sum)
            print("profile_created")
            # csvの該当の日付の行を1にする
            with open("data/profile.csv", "r") as f:
                csv_reader = csv.reader(f)
                rows = [row for row in csv_reader]
            with open("data/profile.csv", "w") as f:
                csv_writer = csv.writer(f)
                for row in rows:
                    if row[0] == today_profile:
                        row[2] = 1
                    csv_writer.writerow(row)
        else:
            logger.info("profileの指定がない")
            d = 0
            break_flg = False
            while True:
                today = datetime.datetime.now() - datetime.timedelta(days=d)
                logger.info('today')
                logger.info(today.strftime('%Y/%-m/%d'))
                
                with open("data/profile.csv", "r") as f:
                    csv_reader = csv.reader(f)
                    for row in csv_reader:
                        print(row[0])
                        if row[0] == today.strftime('%Y/%-m/%d'):
                            today_profile = ''
                            profile_sum = int(row[1])
                            break_flg = True
                            break
                d += 1
                if d > 60:
                    profile_sum = 100
                    profile_create(profile_sum)
                    print("profile_created")
                    break_flg = True
                    break

                if break_flg:
                    break


        if now > start_time and now < end_time:
            
            UA = search.iloc[i]["UA"]
            search_word = search.iloc[i]["検索ワード"]

            Location_name = search.iloc[i]["location"]

            logger.info(Location_name == "0")
            logger.info(Location_name)
            
            if Location_name == "0":
                latitude = 0
                longitude = 0
            elif Location_name == "":
                latitude = 0
                longitude = 0
            elif Location_name not in location.index:
                latitude = 0
                longitude = 0
            else:
                # location 一番上のものを取得
                latitude = location.at[Location_name,'latitude']
                longitude = location.at[Location_name,'longitude']
                try:
                    if len(latitude) > 1:
                        latitude = latitude.iloc[0]
                        longitude = longitude.iloc[0]
                except:
                    pass

            logger.info('latitude')
            logger.info(latitude)
            logger.info('longitude')
            logger.info(longitude)


            logger.info(start_time)
            logger.info(end_time)

            if search.iloc[i]["exec_count"] >= search.iloc[i]["検索上限"]:
                logger.info("検索上限に達したので次の検索に移ります")
                continue

            

            
            work(airplane_mode, latitude,longitude, search_word, '', UA)				
            print(search.iloc[i]["exec_count"])
            search.iat[i, 8] = search.iloc[i]["exec_count"] + 1.0



            search.iat[i, 7] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            print(search.iloc[i]["exec_count"])
            search.to_csv("data/search.csv")
            no_search_flg = True
            logger.info(f'検索間隔{int(search.iloc[i]["検索間隔"])}分です。')
            time.sleep(int(search.iloc[i]['検索間隔']) * 60)
            logger.info(f'検索を開始します。')