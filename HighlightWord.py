import sublime
import sublime_plugin
import sys

IGNORE_CASE = False


class HighlightWordCommand(sublime_plugin.WindowCommand):
    def highlight(self, word_list):
        flag = 0
        view = self.window.active_view()
        self.window.run_command("unhighlight_word")
        flag |= sublime.LITERAL
        if IGNORE_CASE:
            flag |= sublime.IGNORECASE
        for word in word_list:
            region = view.find_all(word, flag)
            view.add_regions(word, region, 'string', '',
                            sublime.HIDE_ON_MINIMAP)
        view.settings().set("highlight_words", word_list)

    def run(self):
        view = self.window.active_view()
        if not view:
            return
        word_list = view.settings().get("highlight_words", [])
        for region in view.sel():
            region = region.empty() and view.word(region) or region
            cursor_word = view.substr(region).strip()
            if cursor_word in word_list:
                word_list.remove(cursor_word)
            else:
                word_list.append(cursor_word)
            break
        self.highlight(word_list)


class UnhighlightWordCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.active_view()
        if not view:
            return
        word_list = view.settings().get("highlight_words", [])
        for region in view.sel():
            region = region.empty() and view.word(region) or region
            cursor_word = view.substr(region).strip()
            if cursor_word in word_list:
                view.erase_regions(cursor_word)
                word_list.remove(cursor_word)
            break
        view.settings().set("highlight_words", word_list)
