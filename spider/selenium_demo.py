from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
# 进入浏览器设置
options = webdriver.ChromeOptions()
# 更换头部
options.add_argument(
    'user-agent=Mozilla/5.0 (Linux; U; win 8.0.0; zh-CN; DUK-AL20 Build/HUAWEIDUK-AL20) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.4.974 UWS/2.14.0.2 Mobile Safari/537.36 AliApp(TB/7.7.5) UCBS/2.11.1.1 TTID/227200@taobao_win_7.7.5 WindVane/8.3.0 1440X2408'
)
options.add_argument('f-refer=wv_h5')
browser = webdriver.Chrome(chrome_options=options)
browser.get('https://login.taobao.com/member/login.jhtml')
time.sleep(30)
# 删除Cookie
browser.delete_all_cookies()
browser.get('https://login.taobao.com/member/login.jhtml')
# 获取商品并输出
elem_good_list = browser.find_element_by_id("J_box_cgf")
elem_goods_names = elem_good_list.find_elements_by_class_name("goods-name")
print(len(elem_goods_names))
for item in elem_goods_names:
    print(item.text)
# 鼠标移动到模式登录
action = ActionChains(browser)
elem_login = browser.find_elements_by_xpath("//*[@id='site_userinfo']/a")[0]
action.move_to_element(elem_login).perform()
# 鼠标移动返还登录,点击返还登录
# elem_fanhuan_login = browser.find_element_by_xpath(
#     "//*[@id='site_userinfo']//*[@class='newshowbox']/a[1]")
# action.move_to_element(elem_fanhuan_login).perform()
# action.click().perform()

# 触发脚本登录
browser.execute_script('Login()')

time.sleep(10)

browser.quit()