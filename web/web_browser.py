import scent
import webview
import time
import datetime
import traceback
import json
from typing import List


class WebBrowser(scent.Object):
    """WEBブラウザのクラス。
    """

    def __init__(self, title: str = None):
        if webview.__doc__.find("pywebview") == -1:
            raise ModuleNotFoundError("Requires installation of pywebview!")
        
        self._window = webview.create_window("", "")
        self._debug = False
        self._tasks = []
        self._previous_task_timestamp = 0
        self._interval_seconds = 1
        self._timeout_seconds = 30
        self._title = title
        self._selected_elements = []
    
    @property
    def debug(self) -> bool:
        return self._debug
    
    @debug.setter
    def debug(self, debug: bool):
        self._debug = debug

    @property
    def interval_seconds(self) -> int:
        return self._interval_seconds
    
    @interval_seconds.setter
    def interval_seconds(self, seconds: int):
        self._interval_seconds = seconds

    @property
    def timeout_seconds(self) -> int:
        return self._timeout_seconds
    
    @timeout_seconds.setter
    def timeout_seconds(self, seconds: int):
        return self._timeout_seconds

    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, title: str):
        self._title = title
        self.update_title()
    
    def update_title(self):
        """ウィンドウタイトルを最新の状態に更新する。
        """
        title = self._title
        if title is None:
            try:
                title = self._window.get_elements("title")[0]["innerText"]
            except Exception:
                return
        self._window.set_title(title)
    
    def get_selected_elements(self) -> list["scent.Element"]:
        """select系のメソッドにより選択状態にある要素をすべて取得する。
        """
        return self._selected_elements
    
    def get_selected_element(self) -> "scent.Element":
        """select系のメソッドにより選択状態にある要素を取得する。
        """
        if self._selected_elements.__len__() == 0:
            return None
        return self._selected_elements[0]

    def set_tasks(self, tasks: tuple | list):
        """ブラウジングを開始した際に実行するタスクをセットする。
        """
        self._tasks = list(tasks)
    
    def add_task(self, task: callable):
        """ブラウジングを開始した際に実行するタスクを追加する。
        """
        self._tasks.append(task)
        
    def _create_tasks_for_running(self):
        self._running_tasks = []
        for index in range(len(self._tasks)):
            self._running_tasks.append(self._tasks[index])
    
    def _create_timeout_error(self) -> scent.TimeoutError:
        message = scent.String("Web browsing flow timed out on task number ")
        message += self._tasks.__len__() - self._running_tasks.__len__()
        message += "."
        return scent.TimeoutError(message)

    def _execute_task(self):
        # 読み込み済みのタイトルを表示
        self.update_title()
        # インターバルとタイムアウト
        if self._tasks.__len__() > self._running_tasks.__len__():
            time.sleep(self._interval_seconds)
        if self._running_tasks.__len__() == 0 or self._closed:
            return
        if self._start_time is not None:
            timeout = self._start_time.copy()
            timeout.add(seconds=self._timeout_seconds)
            if scent.Datetime() > timeout:
                error = self._create_timeout_error()
                self._running_tasks.clear()
                raise error
        self._start_time = scent.Datetime()
        # タスクの実行
        task = self._running_tasks[0]
        self._running_tasks.remove(task)
        previous_url = self.get_url()
        task()
        # タスクによってページ遷移がなければ次のタスクを実行
        time.sleep(0.5)
        if previous_url == self.get_url():
            self._execute_task()

    def show(self):
        """ウィンドウを表示してブラウジングを開始する。
        """
        self._create_tasks_for_running()
        def event_of_loaded():
            self._selected_elements.clear()
            self._execute_task()
        self._window.events.loaded += event_of_loaded
        def event_of_closed():
            self._closed = True
        self._window.events.closed += event_of_closed
        self._start_time = None
        self._closed = False
        webview.start(debug=self.debug)

    def close(self):
        """ウィンドウを閉じる。
        """
        try:
            self._window.destroy()
        except Exception:
            pass

    def get_url(self) -> str:
        """現在のURLを取得する。
        """
        try:
            return self._window.evaluate_js("window.location.href;")
        except Exception:
            return None
    
    def load_url(self, url: str):
        """URLを読み込む。
        """
        self._window.load_url(url)
        if self._title is None:
            self._window.set_title(url)

    def execute_javascript(self, javascript: str) -> str:
        """JavaScriptを実行する。
        """
        try:
            return self._window.evaluate_js(javascript)
        except Exception as exception:
            traceback.print_exception(exception)
            return None
    
    def get_source(self) -> str:
        """現在表示しているページのソースを取得する。
        """
        try:
            return self._window.evaluate_js("document.getElementsByTagName('html')[0].outerHTML;")
        except Exception:
            return None
        
    ELEMENT_ID_PREFIX = "SCENT_WEB_BROWSER_ELEMENT_"

    def _get_element_id(self) -> str:
        self._current_element_id += 1
        id = scent.String(WebBrowser.ELEMENT_ID_PREFIX)
        id += self._current_element_id
        return id.str()
    
    def _create_elements_from_javascript_for_select(self, javascript_for_element_extraction: str) -> List["scent.Element"]:
        timestamp = scent.String(scent.Datetime().value.timestamp()).replace("\.", "").str()
        script = scent.String()
        script += "let result = [];"
        script += "let elements = "
        script += javascript_for_element_extraction
        script += ";"
        script += "let number = 1;"
        script += "elements.forEach((element) => {"
        script += "let id = '"
        script += WebBrowser.ELEMENT_ID_PREFIX
        script += timestamp
        script += "_' + number;"
        script += "number++;"
        script += "element.classList.add(id);"
        script += "result.push(id);"
        script += "});"
        script += "JSON.stringify(result);"
        result = self._window.evaluate_js(script.str())
        elements = []
        for id in json.loads(result):
            elements.append(scent.Element(self, id))
        return elements
    
    def _wait_for_found_by_javascript_for_select(self, javascript_for_element_extraction: str):
        limit = scent.Datetime()
        limit.add(seconds=self._timeout_seconds)
        script = scent.String(javascript_for_element_extraction)
        script += ".length;"
        while limit > scent.Datetime():
            try:
                if scent.String(self._window.evaluate_js(script.str())).to_int() > 0:
                    return
            except Exception:
                pass
            time.sleep(1)
        raise self._create_timeout_error()

    def _make_javascript_for_xpath_to_elements(self, parent_javascript_element: str, xpath: str) -> str:
        script = scent.String("Array.from({ length: (snapshot = document.evaluate(\"")
        script += scent.String(xpath).replace("\"", "'")
        script += "\", "
        script += parent_javascript_element
        script += ", null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null)).snapshotLength }, (_, index) => snapshot.snapshotItem(index))"
        return script.str()

    def select_element_by_xpath(self, xpath: str):
        """XPathに一致する要素を選択状態にする。
        """
        script = self._make_javascript_for_xpath_to_elements("document", xpath)
        elements = self._create_elements_from_javascript_for_select(script)
        self._selected_elements.clear()
        self._selected_elements.extend(elements)

    def select_more_element_by_xpath(self, xpath: str):
        """すでに選択状態にある要素の子要素から、XPathに一致する要素を選択状態にする。
        """
        elements = []
        for element in self._selected_elements:
            script = scent.String(self._make_javascript_for_xpath_to_elements(element._make_javascript_for_element_extraction(), xpath))
            elements.extend(self._create_elements_from_javascript_for_select(script.str()))
        self._selected_elements.clear()
        self._selected_elements.extend(elements)

    def wait_for_found_by_xpath(self, xpath: str):
        """XPathに一致する要素が見つかるのを待機する。
        """
        self._wait_for_found_by_javascript_for_select(self._make_javascript_for_xpath_to_elements("document", xpath))
    
    def _make_xpath_for_attribute(self, name: str, value: str) -> str:
        xpath = scent.String(".//*[@")
        xpath += name
        xpath += "='"
        xpath += value
        xpath += "']"
        return xpath.str()

    def select_element_by_attribute(self, attribute_name: str, attribute_value: str):
        """属性値に一致する要素を選択状態にする。
        """
        self.select_element_by_xpath(self._make_xpath_for_attribute(attribute_name, attribute_value))

    def select_more_element_by_attribute(self, attribute_name: str, attribute_value: str):
        """すでに選択状態にある要素の子要素から、属性値に一致する要素を選択状態にする。
        """
        elements = []
        for element in self._selected_elements:
            script = scent.String(self._make_javascript_for_xpath_to_elements(element._make_javascript_for_element_extraction(), self._make_xpath_for_attribute(attribute_name, attribute_value)))
            elements.extend(self._create_elements_from_javascript_for_select(script.str()))
        self._selected_elements.clear()
        self._selected_elements.extend(elements)

    def wait_for_found_by_attribute(self, attribute_name: str, attribute_value: str):
        """属性値に一致する要素が見つかるのを待機する。
        """
        self._wait_for_found_by_javascript_for_select(self._make_javascript_for_xpath_to_elements("document", self._make_xpath_for_attribute(attribute_name, attribute_value)))
    
    def _make_xpath_for_tag_name(self, tag_name: str, text_content: str) -> str:
        xpath = scent.String(".//")
        xpath += tag_name
        xpath += "[contains(text(), '"
        xpath += text_content
        xpath += "')]"
        return xpath.str()

    def select_element_by_tag_name(self, tag_name: str, text_content: str):
        """タグ名が一致＋テキストを含む要素を選択状態にする。
        """
        self.select_element_by_xpath(self._make_xpath_for_tag_name(tag_name, text_content))

    def select_more_element_by_tag_name(self, tag_name: str, text_content: str):
        """すでに選択状態にある要素の子要素から、タグ名が一致＋テキストを含む要素を選択状態にする。
        """
        elements = []
        for element in self._selected_elements:
            script = scent.String(self._make_javascript_for_xpath_to_elements(element._make_javascript_for_element_extraction(), self._make_xpath_for_tag_name(tag_name, text_content)))
            elements.extend(self._create_elements_from_javascript_for_select(script.str()))
        self._selected_elements.clear()
        self._selected_elements.extend(elements)

    def wait_for_found_by_tag_name(self, tag_name: str, text_content: str):
        """タグ名が一致＋テキストを含む要素が見つかるのを待機する。
        """
        self._wait_for_found_by_javascript_for_select(self._make_javascript_for_xpath_to_elements("document", self._make_xpath_for_tag_name(tag_name, text_content)))

    def select_element_by_css_selector(self, css_selector: str):
        """CSSセレクタに一致する要素を選択状態にする。
        """
        script = scent.String("document.querySelectorAll('")
        script += css_selector
        script += "')"
        elements = self._create_elements_from_javascript_for_select(script.str())
        self._selected_elements.clear()
        self._selected_elements.extend(elements)

    def select_more_element_by_css_selector(self, css_selector: str):
        """すでに選択状態にある要素の子要素から、CSSセレクタに一致する要素を選択状態にする。
        """
        elements = []
        for element in self._selected_elements:
            script = scent.String(element._make_javascript_for_element_extraction())
            script += ".querySelectorAll('"
            script += css_selector
            script += "')"
            elements.extend(self._create_elements_from_javascript_for_select(script.str()))
        self._selected_elements.clear()
        self._selected_elements.extend(elements)

    def wait_for_found_by_css_selector(self, css_selector: str):
        """CSSセレクタに一致する要素が見つかるのを待機する。
        """
        script = scent.String("document.querySelectorAll('")
        script += css_selector
        script += "')"
        self._wait_for_found_by_javascript_for_select(script.str())
