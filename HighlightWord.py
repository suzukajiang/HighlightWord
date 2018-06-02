import sublime
import sublime_plugin
import sys

IGNORE_CASE = False

def highlight(view, word_list):
    if not view:
        return
    flag = 0
    flag |= sublime.LITERAL
    if IGNORE_CASE:
        flag |= sublime.IGNORECASE
    size = 0
    for word in word_list:
        region = view.find_all(word, flag)
        view.add_regions("highlight_key_%d" % size, region,
                         'string', '', sublime.HIDE_ON_MINIMAP)
        size += 1
    view.settings().set("highlight_words", word_list)


def unhighlight(view):
    if not view:
        return
    word_list = view.settings().get("highlight_words", [])
    count = len(word_list)
    for i in range(count):
        view.erase_regions("highlight_key_%d" % i)


class HighlightWordCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view:
            return
        word_list = view.settings().get("highlight_words", [])
        for region in view.sel():
            region = region.empty() and view.word(region) or region
            cursor_word = view.substr(region).strip()
            if cursor_word not in word_list:
                word_list.append(cursor_word)
            else:
                word_list.remove(cursor_word)
        unhighlight(view)
        highlight(view, word_list)


class HighlightWordListener(sublime_plugin.EventListener):
    def on_modified_async(self, view):
        if not view:
            return
        word_list = view.settings().get("highlight_words", [])
        if len(word_list) is 0:
            return
        unhighlight(view)
        highlight(view, word_list)
