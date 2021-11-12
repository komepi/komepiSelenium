from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from selenium.webdriver.support.select import Select

d=""
XPATH = 0
ID = 1
CLASS = 2
NAME = 3
MSG_NOT_FOUD_ELEMENT = "要素[%s]は存在しません."
MSG_NOT_EXIST_METHOD = "正しい選択手法を選択してください"
METHOD_LIST = [XPATH, ID, CLASS, NAME]
INDEX = 0
VALUE = 1
TEXT = 2
SELECT_LIST = [INDEX, VALUE, TEXT]

def connect_chrome(path: str, url: str, is_watch: bool = True):
    """クロームに接続する

    Args:
        path (str): クロームのウェブドライバーがあるパス
        url (str): 最初に接続するURL
        is_watch (bool, optional): ブラウザ立ち上げの有無（True:立ち上げない, False:立ち上げる). Defaults to True.
    
    Returns:
        webdriver: 使用するウェブドライバー
    """

    # WebDriver のオプションを設定する
    options = webdriver.ChromeOptions()
    global d
    if is_watch:
        options.add_argument('--headless')
    d = webdriver.Chrome(executable_path=path, options = options)

    d.get(url)
    time.sleep(5.0)
    return d

def send_data(d: webdriver, data: str, path: str, method: int, serial: int = None, memo = None):
    
    """htmlにデータを送る
    0:xpath, 1:id, 2:class: 3:name
    Args:
        d (webdriver): 使用するウェブドライバー
        data (str): 送るデータ
        path (str): 要素を検索するデータ
        method (int, optional): 検索手法. Defaults to 0.
        serial (int, optional): 連番 該当要素が複数ある場合. Defaults to 0.
        memo (str, optional): 何のボタンかのメモ用. Defaults to None
    """
    try:
        m = _select_method(method)
    except KeyError:
        print(MSG_NOT_EXIST_METHOD)
    try:
        element = d.find_element(m, path)
    except:
        print(MSG_NOT_FOUD_ELEMENT % path)
        return
    
    element.send_keys(data)

def click(d: webdriver, path: str, method: int, memo = None):
    """要素をクリック
    0:xpath, 1:id, 2:class: 3:name
    Args:
        d (webdriver): 使用するウェブドライバー
        path (str): 要素を検索するデータ
        method (int, optional): 検索手法. Defaults to 0.
        is_check (bool, optional): チェック（読み込みがない）か否か True:チェック, False:チェックでない. Defaults to False.
        span_time (float, optional): 待機時間. Defaults to 1.0.
        memo (str, optional): 何のボタンかメモ用. Defaults to None.
    """
    try:
        m = _select_method(method)
    except KeyError:
        print(MSG_NOT_EXIST_METHOD)

    d.find_element(m, path).click()

def click_with_update(d: webdriver, path: str, method: int, span_time: float = 1.0, memo: str = None)
    """要素を読み込みありでクリック
    
    Args:
        d (webdriver): 使用するウェブドライバー
        path (str): 要素を検索するデータ
        method (int): 検索手法
        span_time (float): 待機時間. Defaults to 1.0.
        memo (str): 何をクリックしたかのメモ用（処理では使わない）
     """
    click(d, path, method)
    time.sleep(span_time)
    
def select_drop(d: webdriver, data: obj, path: str, method: int, select_by: int, memo: str = None):
    """ドロップダウンから選択する
    method -> 0:xpath, 1:id, 2:class, 3:name
    select_by -> 0:index, 1:value, 2:text
    Args:
        d (webdriver): 使用するウェブドライバー
        data (obj): 選択に用いるデータ
        path (str): 要素を検索するデータ
        method (int, optional): 検索手法.
        select_by (int, optional): 選択手法.
        memo (str, optional): 何を選択したかメモ用(処理には使わない). Defaults to None.
    """
    try:
        m = _select_method(method)
    except KeyError:
        print(MSG_NOT_EXIST_METHOD)
    
    select_obj = d.find_element(m,path)

    select = Select(select_obj)
    _select_by(select,select_by,data)
    
def _select_method(method: int):
    """検索手法を探す

    Args:
        method (int): 検索手法の番号

    Raises:
        KeyError: 定められた検索手法番号以外の番号

    Returns:
        by: 検索手法
    """
    if method not in METHOD_LIST:
        raise KeyError
    if method == XPATH:
        m = By.XPATH
    elif method == ID:
        m = By.ID
    elif method == CLASS:
        m = By.CLASS_NAME
    elif method == NAME:
        m = By.NAME

    return m

def _select_by(select: Select, method: int, value: obj):
    """選択する

    Args:
        select (select): selectオブジェクト
        method (int): 選択手法
        value (obj): 選択に用いるデータ

    Raises:
        KeyError: 定められた選択手法以外の番号

    """
    if method not in SELECT_LIST:
        raise KeyError
    if method == INDEX:
        return select.select_by_index(value)
    elif method == VALUE:
        print("select by value to " + value)
        select.select_by_value(value)
    elif method == TEXT:
        select.select_by_visible_text(value)
