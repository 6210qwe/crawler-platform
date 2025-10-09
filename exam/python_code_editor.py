import sys
import re
import traceback
import keyword
from io import StringIO
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt5.QtGui import (
    QSyntaxHighlighter,
    QTextCharFormat,
    QFont,
    QColor,
    QTextCursor,
    QTextBlockFormat
)
from PyQt5.QtWidgets import (
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QPushButton,
    QMessageBox,
    QSplitter,
    QApplication
)


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(128, 0, 128))
        self.keyword_format.setFontWeight(QFont.Bold)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(0, 128, 0))

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(128, 128, 128))

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(255, 165, 0))

        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor(0, 0, 255))

        self.keywords = keyword.kwlist

        self.patterns = [
            (re.compile(rf"\b{kw}\b"), self.keyword_format) for kw in self.keywords
        ]
        self.patterns.extend([
            (re.compile(r'"[^"\\]*(\\.[^"\\]*)*"'), self.string_format),
            (re.compile(r"'[^'\\]*(\\.[^'\\]*)*'"), self.string_format),
            (re.compile(r"\b[0-9]+\b"), self.number_format),
            (re.compile(r"\b[A-Za-z0-9_]+(?=\()"), self.function_format),
            (re.compile(r"#.*$"), self.comment_format)
        ])

    def highlightBlock(self, text):
        try:
            for pattern, fmt in self.patterns:
                for match in pattern.finditer(text):
                    start = match.start()
                    self.setFormat(start, match.end() - start, fmt)
        except Exception:
            pass


class CodeExecutor(QThread):
    output_ready = pyqtSignal(str)

    def __init__(self, code):
        super().__init__()
        self.code = code
        self.setTerminationEnabled(True)

    def run(self):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = StringIO()
        sys.stdout = redirected_output
        sys.stderr = redirected_output

        try:
            clean_code = re.sub(
                r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x8F\u2029]',
                '\n',
                self.code
            )
            exec(clean_code, {})
            output = redirected_output.getvalue()
            self.output_ready.emit(f"输出:\n{output}" if output else "代码执行成功，无输出")
        except Exception:
            self.output_ready.emit(f"错误:\n{traceback.format_exc()}")
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


class CodeTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.indent_width = 4
        self.CODE_BLOCK_START = "```"
        self.init_ui()

    def init_ui(self):
        self.setAcceptRichText(False)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setTabStopWidth(self.indent_width * self.fontMetrics().width(' '))

        font = QFont()
        font.setFamily("Consolas, Microsoft YaHei, SimHei")
        font.setPointSize(10)
        self.setFont(font)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #333;
                border: 1px solid #ccc;
                padding: 10px;
            }
        """)

        self.highlighter = PythonHighlighter(self.document())
        self.textChanged.connect(self.refresh_code_blocks)

    def insert_code_block(self):
        self.textChanged.disconnect(self.refresh_code_blocks)

        cursor = self.textCursor()
        cursor.insertText(f"{self.CODE_BLOCK_START}python\n\n{self.CODE_BLOCK_START}\n")
        cursor.movePosition(QTextCursor.Up)
        cursor.movePosition(QTextCursor.Up)
        self.setTextCursor(cursor)

        self.refresh_code_blocks()
        self.textChanged.connect(self.refresh_code_blocks)

    def refresh_code_blocks(self):
        try:
            self.textChanged.disconnect(self.refresh_code_blocks)
        except Exception:
            pass

        self._clear_all_format()

        block = self.document().firstBlock()
        in_code_block = False
        code_block_start_line = -1

        while block.isValid():
            text = block.text().strip()
            current_line = block.blockNumber()

            if text.startswith(self.CODE_BLOCK_START):
                in_code_block = not in_code_block
                if in_code_block:
                    code_block_start_line = current_line
                else:
                    self._format_code_block(code_block_start_line, current_line)

            block = block.next()

        self.textChanged.connect(self.refresh_code_blocks)

    def _format_code_block(self, start_line, end_line):
        if start_line >= end_line - 1:
            return

        code_block_fmt = QTextBlockFormat()
        code_block_fmt.setLeftMargin(20)
        code_block_fmt.setBackground(QColor(245, 245, 245))

        block = self.document().findBlockByNumber(start_line + 1)
        while block.isValid() and block.blockNumber() < end_line:
            cursor = QTextCursor(block)
            cursor.setBlockFormat(code_block_fmt)
            block = block.next()

    def _clear_all_format(self):
        cursor = QTextCursor(self.document())
        cursor.select(QTextCursor.Document)
        normal_fmt = QTextBlockFormat()
        normal_fmt.setLeftMargin(0)
        normal_fmt.setBackground(QColor(255, 255, 255))
        cursor.setBlockFormat(normal_fmt)

    def get_selected_code(self):
        cursor = self.textCursor()
        if not cursor.hasSelection():
            return None

        selected_text = cursor.selectedText().replace('\u2029', '\n')
        start_block = self.document().findBlock(cursor.selectionStart())

        if start_block.blockFormat().leftMargin() == 20:
            return selected_text
        return None

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        current_block = cursor.block()
        in_code_block = current_block.blockFormat().leftMargin() == 20

        if event.key() == Qt.Key_Tab and in_code_block:
            self.insertPlainText(' ' * self.indent_width)
            return

        elif event.key() == Qt.Key_Backspace and in_code_block:
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, cursor.columnNumber())
            selected_text = cursor.selectedText()
            if selected_text == ' ' * self.indent_width:
                cursor.removeSelectedText()
                return

        elif event.key() in (Qt.Key_Return, Qt.Key_Enter) and in_code_block:
            cursor.select(QTextCursor.LineUnderCursor)
            current_line = cursor.selectedText()
            cursor.clearSelection()

            current_indent = self._calculate_indent(current_line)
            line_stripped = current_line.rstrip()

            if line_stripped.endswith(':') and not self._in_string(current_line):
                new_indent = current_indent + self.indent_width
            else:
                new_indent = current_indent
                new_indent = self._adjust_for_closing_brackets(current_line, new_indent)

            cursor.insertText('\n' + ' ' * new_indent)
            return

        super().keyPressEvent(event)

        if in_code_block and event.text() in '})]':
            self._auto_unindent()

    def _calculate_indent(self, line):
        indent = 0
        for c in line:
            if c == ' ':
                indent += 1
            else:
                break
        return indent

    def _in_string(self, line):
        in_single_quote = False
        in_double_quote = False
        for c in line:
            if c == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            elif c == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
        return in_single_quote or in_double_quote

    def _adjust_for_closing_brackets(self, line, current_indent):
        stripped_line = line.strip()
        if stripped_line.startswith(('}', ')', ']')):
            return max(0, current_indent - self.indent_width)
        return current_indent

    def _auto_unindent(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Up)
        cursor.movePosition(QTextCursor.EndOfLine)
        line = cursor.block().text()

        if line.strip().endswith((':', '{', '(', '[')):
            current_indent = self._calculate_indent(line)
            if current_indent > 0:
                cursor.movePosition(QTextCursor.Down)
                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, self.indent_width)
                if cursor.selectedText() == ' ' * self.indent_width:
                    cursor.removeSelectedText()


class PythonCodeEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.executor = None
        self.splitter = None  # 保存splitter引用
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # 保存splitter引用，方便后续操作
        self.splitter = QSplitter(Qt.Vertical)
        # 禁止折叠输出框
        self.splitter.setCollapsible(1, False)

        self.code_edit = CodeTextEdit()
        self.splitter.addWidget(self.code_edit)

        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        self.output_edit.setStyleSheet("""
            QTextEdit {
                background-color: #f8f8f8;
                color: #333;
                border: 1px solid #ccc;
                padding: 10px;
            }
        """)
        # 设置最小高度，防止被压缩到看不见
        self.output_edit.setMinimumHeight(100)
        # 初始隐藏输出框
        self.output_edit.setVisible(False)
        self.splitter.addWidget(self.output_edit)
        self.splitter.setSizes([400, 200])

        btn_layout = QHBoxLayout()
        self.insert_btn = QPushButton("插入代码块")
        self.insert_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px 10px;")
        self.insert_btn.clicked.connect(self.code_edit.insert_code_block)

        self.run_btn = QPushButton("执行选中代码")
        self.run_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 5px 10px;")
        self.run_btn.clicked.connect(self.run_code)

        self.clear_btn = QPushButton("清空输出")
        self.clear_btn.setStyleSheet("background-color: #f44336; color: white; padding: 5px 10px;")
        self.clear_btn.clicked.connect(self.clear_output)

        btn_layout.addWidget(self.insert_btn)
        btn_layout.addWidget(self.run_btn)
        btn_layout.addWidget(self.clear_btn)

        main_layout.addWidget(self.splitter)
        main_layout.addLayout(btn_layout)

    def run_code(self):
        code = self.code_edit.get_selected_code()
        if not code:
            QMessageBox.warning(self, "提示", "请先在代码块中选中要执行的代码！")
            return

        if self.executor and self.executor.isRunning():
            self.executor.terminate()
            self.output_edit.setText("已终止上一次代码执行")

        # 执行前显示输出框
        self.output_edit.setVisible(True)
        self.executor = CodeExecutor(code)
        # 连接到专门的处理函数，确保输出后滚动到视野
        self.executor.output_ready.connect(self.handle_output)
        self.executor.start()

    def handle_output(self, output_text):
        """处理输出内容并确保输出框可见"""
        self.output_edit.setText(output_text)

        # 确保输出框可见并滚动到顶部
        self.output_edit.setVisible(True)

        # 重置splitter尺寸，确保输出框有足够高度
        current_sizes = self.splitter.sizes()
        # 如果输出框高度太小，调整它
        if current_sizes[1] < 100:
            self.splitter.setSizes([current_sizes[0], 200])

        # 滚动到输出框内容顶部
        cursor = self.output_edit.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.output_edit.setTextCursor(cursor)

        # 确保输出框获得焦点，视觉上更明显
        self.output_edit.setFocus()

    def clear_output(self):
        self.output_edit.clear()
        # 清空后隐藏输出框
        self.output_edit.setVisible(False)

    def setText(self, text):
        self.code_edit.setPlainText(text)
        self.code_edit.refresh_code_blocks()

    def toPlainText(self):
        return self.code_edit.toPlainText()

    def setPlainText(self, text):
        self.code_edit.textChanged.disconnect(self.code_edit.refresh_code_blocks)
        self.code_edit.setPlainText(text)
        self.code_edit.refresh_code_blocks()
        self.code_edit.textChanged.connect(self.code_edit.refresh_code_blocks)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     editor = PythonCodeEditor()
#     # 设置初始代码示例
#     initial_code = """这是一个简单的Python代码编辑器示例
# # 使用方法:
# 1. 点击"插入代码块"按钮创建代码区域
# 2. 在代码块中编写Python代码
# 3. 选中要执行的代码
# 4. 点击"执行选中代码"按钮运行
#
# 示例代码:def greet(name):
#     return f"Hello, {name}!"
#
# # 测试函数
# print(greet("World"))
#
# # 列表推导式示例
# numbers = [1, 2, 3, 4, 5]
# squared = [x**2 for x in numbers]
# print("平方结果:", squared)
#
# # 循环示例
# for i in range(3):
#     print(f"循环第 {i+1} 次")"""
#     editor.setPlainText(initial_code)
#     editor.setWindowTitle("Python代码编辑器")
#     editor.resize(800, 600)
#     editor.show()
#     sys.exit(app.exec_())
