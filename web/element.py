import scent_python as scent


class Element(scent.Object):
    """WEBページの要素のクラス。
    """

    def __init__(self, web_browser: scent.WebBrowser, id: str):
        self._web_browser = web_browser
        self._id = id

    def _make_javascript_for_element_extraction(self) -> str:
        return "document.getElementsByClassName('" + self._id + "')[0]"
    
    def get_tag_name(self) -> str:
        """要素のタグ名を取得する。
        """
        return scent.String(self._web_browser._window.evaluate_js(self._make_javascript_for_element_extraction() + ".tagName;")).lower().str()
    
    def get_source(self) -> str:
        """要素のソースを取得する。
        """
        return self._web_browser._window.evaluate_js(self._make_javascript_for_element_extraction() + ".outerHTML;")

    def get_text_content(self) -> str:
        """要素が内包する文字列を取得する。
        """
        return self._web_browser._window.evaluate_js(self._make_javascript_for_element_extraction() + ".innerText;")
    
    def set_text_content(self, text: str):
        """要素が内包する文字列をセットする。
        """
        self._web_browser._window.evaluate_js(self._make_javascript_for_element_extraction() + ".innerText = '" + text + "';")
    
    def get_attribute(self, name: str) -> str:
        """要素の属性値を取得する。
        """
        return self._web_browser._window.evaluate_js(self._make_javascript_for_element_extraction() + ".getAttribute('" + name + "');")
    
    def set_attribute(self, name: str, value: str):
        """要素の属性値をセットする。
        """
        self._web_browser._window.evaluate_js(self._make_javascript_for_element_extraction() + ".setAttribute('"+ name + "', '" + value + "');")
    
    def remove_attribute(self, name: str):
        """要素の属性値を削除する。
        """
        self._web_browser._window.evaluate_js(self._make_javascript_for_element_extraction() + ".removeAttribute('"+ name + "');")

    def click(self):
        """要素をクリックする。
        """
        self._web_browser._window.evaluate_js(self._make_javascript_for_element_extraction() + ".click();")
    
    def get_selected_options(self) -> list["Element"]:
        """select要素内で選択されているoption要素の値を取得する。
        """
        script = scent.String()
        script += "Array.from("
        script += self._make_javascript_for_element_extraction()
        script += ".selectedOptions);"
        return self._web_browser._create_elements_from_javascript_for_select(script.str())
    
    def add_selected_options(self, value: str):
        """select要素内で指定された値を持つoption要素を選択状態にする。
        """
        script = scent.String()
        script += "Array.from("
        script += self._make_javascript_for_element_extraction()
        script += ".children).forEach((element) => {"
        script += "if (element.value == '"
        script += value
        script += "') {"
        script += "element.selected = true;"
        script += "}"
        script += "});"
        self._web_browser._window.evaluate_js(script.str())

    def clear_selected_options(self):
        """select要素内のすべてのoption要素を未選択状態にする。
        """
        script = scent.String()
        script += "Array.from("
        script += self._make_javascript_for_element_extraction()
        script += ".children).forEach((element) => {"
        script += "element.selected = false;"
        script += "});"
        self._web_browser._window.evaluate_js(script.str())

    def get_parent(self) -> "Element":
        """親要素を取得する。
        """
        script = scent.String()
        script += "["
        script += self._make_javascript_for_element_extraction()
        script += ".parentNode]"
        elements = self._web_browser._create_elements_from_javascript_for_select(script.str())
        if elements.__len__() == 0:
            return None
        return elements[0]
    
    def get_children(self) -> list["Element"]:
        """子要素要素を取得する。
        """
        script = scent.String()
        script += "Array.from("
        script += self._make_javascript_for_element_extraction()
        script += ".children);"
        return self._web_browser._create_elements_from_javascript_for_select(script.str())
