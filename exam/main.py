import sys
import json
import openpyxl
import random
import pymysql
from PyQt5 import QtGui
from PyQt5.QtGui import QIntValidator
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QListWidget, QStackedWidget, QMessageBox,
                             QLineEdit, QTextEdit, QRadioButton, QCheckBox, QComboBox,
                             QGroupBox, QDialog, QFormLayout, QInputDialog, QFileDialog,
                             QTreeWidget, QTreeWidgetItem, QAbstractItemView, QTabWidget)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap
import matplotlib.pyplot as plt
from get_mysqldb import DatabasePool
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from loguru import logger

from python_code_editor import PythonCodeEditor  # 直接导入封装后的组件


class BrainyQuiz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("爬虫基础知识复习")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet(self.get_stylesheet())
        # 初始化数据
        self.current_question_bank = None
        self.question_banks = {}
        self.current_questions = []
        self.current_index = 0
        self.user_answers = {}
        self.wrong_questions = {}
        self.exam_mode = False
        self.practice_mode = False
        self.score = 0
        self.total_score = 0
        self.practice_order = "顺序"
        # 创建主界面
        self.init_ui()
        self.DB_HOST = "127.0.0.1"
        self.DB_PORT = 3306
        self.DB_DATABASE = "question_bank"
        self.DB_USER = "root"
        self.DB_PASSWORD = "root"
        self.mysql_db = DatabasePool(
            logger=logger,
            DB_HOST=self.DB_HOST,
            DB_PORT=self.DB_PORT,
            DB_DATABASE=self.DB_DATABASE,
            DB_USER=self.DB_USER,
            DB_PASSWORD=self.DB_PASSWORD
        )
        # 加载题库列表
        self.load_question_bank_list()

    def get_stylesheet(self):
        """返回应用程序样式表"""
        return """
            QMainWindow {
                background-color: #f5f7fa;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #4e73df;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #3a5fcd;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QListWidget, QTreeWidget, QTextEdit, QLineEdit, QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
            }
            QRadioButton, QCheckBox {
                spacing: 5px;
            }
        """

    def init_ui(self):
        """初始化UI界面"""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        # 左侧导航栏
        self.create_sidebar()

        # 右侧内容区域
        self.content_area = QStackedWidget()

        # 添加各个页面
        self.create_all_pages()

        # 将侧边栏和内容区域添加到主布局
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content_area)

    def create_sidebar(self):
        """创建左侧导航栏"""
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: #2c3e50;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)

        # 应用标题
        title = QLabel("🎓 爬虫基础知识")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 20px 10px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(title)

        # 导航按钮
        self.create_navigation_buttons()

        # 添加按钮到侧边栏
        self.sidebar_layout.addStretch()
        self.sidebar_layout.addWidget(self.btn_exit)

    def create_navigation_buttons(self):
        """创建导航按钮"""
        self.btn_bank = QPushButton("📂 题库管理")
        self.btn_bank.setStyleSheet("text-align: left; padding-left: 20px;")
        self.btn_bank.clicked.connect(self.show_bank_manager)

        self.btn_exam = QPushButton("📋 随机组卷")
        self.btn_exam.setStyleSheet("text-align: left; padding-left: 20px;")
        self.btn_exam.clicked.connect(self.show_exam_setup)

        self.btn_practice = QPushButton("🌊 题海刷题")
        self.btn_practice.setStyleSheet("text-align: left; padding-left: 20px;")
        self.btn_practice.clicked.connect(self.show_practice_setup)

        self.btn_wrong = QPushButton("❌ 错题集")
        self.btn_wrong.setStyleSheet("text-align: left; padding-left: 20px;")
        self.btn_wrong.clicked.connect(self.show_wrong_questions)

        self.btn_stats = QPushButton("📈 学习统计")
        self.btn_stats.setStyleSheet("text-align: left; padding-left: 20px;")
        self.btn_stats.clicked.connect(self.show_stats)

        self.btn_exit = QPushButton("🚪 退出")
        self.btn_exit.setStyleSheet("text-align: left; padding-left: 20px;")
        self.btn_exit.clicked.connect(self.close)

        # 添加按钮到侧边栏
        buttons = [self.btn_bank, self.btn_exam, self.btn_practice,
                   self.btn_wrong, self.btn_stats]
        for btn in buttons:
            self.sidebar_layout.addWidget(btn)

    def create_all_pages(self):
        """创建所有内容页面"""
        self.main_page = self.create_main_page()
        self.bank_manager_page = self.create_bank_manager_page()
        self.bank_editor_page = self.create_bank_editor_page()
        self.exam_setup_page = self.create_exam_setup_page()
        self.exam_page = self.create_exam_page()
        self.result_page = self.create_result_page()
        self.wrong_questions_page = self.create_wrong_questions_page()
        self.stats_page = self.create_stats_page()
        self.practice_setup_page = self.create_practice_setup_page()
        self.practice_page = self.create_practice_page()

        # 添加到堆栈窗口
        pages = [
            self.main_page, self.bank_manager_page, self.bank_editor_page,
            self.exam_setup_page, self.exam_page, self.result_page,
            self.wrong_questions_page, self.stats_page,
            self.practice_setup_page, self.practice_page
        ]
        for page in pages:
            self.content_area.addWidget(page)

    def create_main_page(self):
        """创建主页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        title = QLabel("点亮你的题海修行之路")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 30px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 应用描述
        desc = QLabel("一款功能强大的刷题软件，支持多种题型和智能学习统计")
        desc.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        # 插入空行
        spacer = QLabel("")
        spacer.setFixedHeight(15)  # 设置高度，10~20px 之间都可以
        layout.addWidget(spacer)

        # 图标（如果没有资源文件则不显示）
        icon = QLabel()
        try:
            pixmap = QPixmap("icon.ico")
            if not pixmap.isNull():
                pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon.setPixmap(pixmap)
                icon.setAlignment(Qt.AlignCenter)
                layout.addWidget(icon)
        except:
            pass

        layout.addStretch()
        return page

    def create_bank_manager_page(self):
        """创建题库管理页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        title = QLabel("📂 题库管理")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 题库列表
        self.bank_list = QListWidget()
        self.bank_list.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.bank_list)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.btn_new_bank = QPushButton("➕ 新建题库")
        self.btn_new_bank.clicked.connect(self.create_new_bank)

        self.btn_import_bank = QPushButton("📥 导入题库")
        self.btn_import_bank.clicked.connect(self.import_question_bank)

        self.btn_edit_bank = QPushButton("✏️ 编辑题库")
        self.btn_edit_bank.clicked.connect(self.edit_selected_bank)

        self.btn_export_bank = QPushButton("📤 导出题库")
        self.btn_export_bank.clicked.connect(self.export_selected_bank)

        self.btn_delete_bank = QPushButton("🗑️ 删除题库")
        self.btn_delete_bank.clicked.connect(self.delete_selected_bank)

        buttons = [self.btn_new_bank, self.btn_import_bank, self.btn_edit_bank,
                   self.btn_export_bank, self.btn_delete_bank]
        for btn in buttons:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        # 返回按钮
        self.btn_back = QPushButton("🔙 返回")
        self.btn_back.clicked.connect(self.show_main_page)
        layout.addWidget(self.btn_back, alignment=Qt.AlignRight)

        return page

    def create_bank_editor_page(self):
        """创建题库编辑器页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        self.bank_editor_title = QLabel()
        self.bank_editor_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        self.bank_editor_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.bank_editor_title)

        # 题目列表
        self.question_tree = QTreeWidget()
        self.question_tree.setHeaderLabels(["题型", "题目", "选项", "答案", "分值"])
        self.question_tree.setColumnWidth(0, 80)
        self.question_tree.setColumnWidth(1, 300)
        self.question_tree.setColumnWidth(2, 200)
        self.question_tree.setColumnWidth(3, 100)
        self.question_tree.setColumnWidth(4, 60)
        self.question_tree.setSelectionMode(QAbstractItemView.SingleSelection)

        # 设置行高
        row_height = 30  # 可以根据实际需求调整这个值
        self.question_tree.setStyleSheet(f"QTreeView::item {{ height: {row_height}px; }}")

        layout.addWidget(self.question_tree)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.btn_add_question = QPushButton("➕ 添加题目")
        self.btn_add_question.clicked.connect(self.add_question_dialog)

        self.btn_edit_question = QPushButton("✏️ 编辑题目")
        self.btn_edit_question.clicked.connect(self.edit_question_dialog)

        self.btn_delete_question = QPushButton("🗑️ 删除题目")
        self.btn_delete_question.clicked.connect(self.delete_question)

        buttons = [self.btn_add_question, self.btn_edit_question, self.btn_delete_question]
        for btn in buttons:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        # 保存和返回按钮
        bottom_btn_layout = QHBoxLayout()

        self.btn_save_bank = QPushButton("💾 保存题库")
        self.btn_save_bank.clicked.connect(self.save_question_bank)

        self.btn_back_editor = QPushButton("🔙 返回")
        self.btn_back_editor.clicked.connect(self.show_bank_manager)

        bottom_btn_layout.addWidget(self.btn_save_bank)
        bottom_btn_layout.addStretch()
        bottom_btn_layout.addWidget(self.btn_back_editor)

        layout.addLayout(bottom_btn_layout)

        return page

    def create_exam_setup_page(self):
        """创建组卷设置页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        self.exam_setup_title = QLabel("📋 随机组卷设置")
        self.exam_setup_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        self.exam_setup_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.exam_setup_title)

        # 设置表单
        form_layout = QFormLayout()

        # 题库选择
        self.bank_combo = QComboBox()
        form_layout.addRow("选择题库:", self.bank_combo)

        # 组卷设置
        self.exam_settings_group = QGroupBox("组卷设置")
        exam_layout = QVBoxLayout(self.exam_settings_group)

        # 题目数量
        self.num_questions = QLineEdit("10")
        self.num_questions.setValidator(QtGui.QIntValidator(1, 100))
        exam_layout.addWidget(QLabel("题目数量:"))
        exam_layout.addWidget(self.num_questions)

        # 题型分布
        type_layout = QHBoxLayout()

        self.single_ratio = QLineEdit("40")
        self.single_ratio.setValidator(QtGui.QIntValidator(0, 100))
        type_layout.addWidget(QLabel("单选:"))
        type_layout.addWidget(self.single_ratio)
        type_layout.addWidget(QLabel("%"))

        self.multi_ratio = QLineEdit("30")
        self.multi_ratio.setValidator(QtGui.QIntValidator(0, 100))
        type_layout.addWidget(QLabel("多选:"))
        type_layout.addWidget(self.multi_ratio)
        type_layout.addWidget(QLabel("%"))

        self.bool_ratio = QLineEdit("30")
        self.bool_ratio.setValidator(QtGui.QIntValidator(0, 100))
        type_layout.addWidget(QLabel("判断:"))
        type_layout.addWidget(self.bool_ratio)
        type_layout.addWidget(QLabel("%"))

        exam_layout.addWidget(QLabel("题型分布:"))
        exam_layout.addLayout(type_layout)

        # 时间限制
        self.time_limit_label = QLabel("时间限制(分钟):")
        self.time_limit = QLineEdit("30")
        self.time_limit.setValidator(QtGui.QIntValidator(1, 300))
        exam_layout.addWidget(self.time_limit_label)
        exam_layout.addWidget(self.time_limit)

        form_layout.addRow(self.exam_settings_group)

        layout.addLayout(form_layout)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.btn_start_exam = QPushButton("📝 开始考试")
        self.btn_start_exam.clicked.connect(self.start_exam)

        self.btn_back_setup = QPushButton("🔙 返回")
        self.btn_back_setup.clicked.connect(self.show_main_page)

        btn_layout.addWidget(self.btn_start_exam)
        btn_layout.addWidget(self.btn_back_setup)

        layout.addLayout(btn_layout)

        return page

    # def create_exam_page(self):
    #     """创建考试页面"""
    #     page = QWidget()
    #     layout = QVBoxLayout(page)
    #
    #     # 计时器
    #     self.timer_layout = QHBoxLayout()
    #     self.timer_label = QLabel()
    #     self.timer_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")
    #     self.timer_layout.addStretch()
    #     self.timer_layout.addWidget(self.timer_label)
    #     layout.addLayout(self.timer_layout)
    #
    #     # 进度显示
    #     self.progress_label = QLabel()
    #     self.progress_label.setStyleSheet("font-size: 16px; font-weight: bold;")
    #     layout.addWidget(self.progress_label, alignment=Qt.AlignLeft)
    #
    #     # 题目内容
    #     self.question_group = QGroupBox()
    #     self.question_group.setStyleSheet("QGroupBox { font-size: 14px; }")
    #     question_layout = QVBoxLayout(self.question_group)
    #
    #     self.question_type_label = QLabel()
    #     self.question_type_label.setStyleSheet("font-weight: bold; color: #3498db;")
    #
    #     self.question_text = QLabel()
    #     self.question_text.setWordWrap(True)
    #     self.question_text.setStyleSheet("font-size: 15px;")
    #
    #     self.options_layout = QVBoxLayout()
    #
    #     question_layout.addWidget(self.question_type_label)
    #     question_layout.addWidget(self.question_text)
    #     question_layout.addLayout(self.options_layout)
    #     question_layout.addStretch()
    #
    #     layout.addWidget(self.question_group)
    #
    #     # 按钮区域
    #     btn_layout = QHBoxLayout()
    #
    #     self.btn_prev = QPushButton("⬅️ 上一题")
    #     self.btn_prev.clicked.connect(self.prev_question)
    #
    #     self.btn_next = QPushButton("➡️ 下一题")
    #     self.btn_next.clicked.connect(self.next_question)
    #
    #     self.btn_submit = QPushButton("📝 交卷")
    #     self.btn_submit.clicked.connect(self.submit_exam)
    #
    #     self.btn_back_exam = QPushButton("🔙 返回")
    #     self.btn_back_exam.clicked.connect(self.confirm_exit_exam)
    #
    #     buttons = [self.btn_prev, self.btn_next, self.btn_submit, self.btn_back_exam]
    #     for btn in buttons:
    #         btn_layout.addWidget(btn)
    #
    #     layout.addLayout(btn_layout)
    #
    #     return page

    def create_exam_page(self):
        """创建考试页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 计时器
        self.timer_layout = QHBoxLayout()
        self.timer_label = QLabel()
        self.timer_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c;")
        self.timer_layout.addStretch()
        self.timer_layout.addWidget(self.timer_label)
        layout.addLayout(self.timer_layout)

        # 进度显示
        self.progress_label = QLabel()
        self.progress_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.progress_label, alignment=Qt.AlignLeft)

        # 题目内容
        self.question_group = QGroupBox()
        self.question_group.setStyleSheet("QGroupBox { font-size: 14px; }")
        question_layout = QVBoxLayout(self.question_group)

        self.question_type_label = QLabel()
        self.question_type_label.setStyleSheet("font-weight: bold; color: #3498db;")

        self.question_text = QLabel()
        self.question_text.setWordWrap(True)
        self.question_text.setStyleSheet("font-size: 15px;")

        self.options_layout = QVBoxLayout()

        # 添加填空题和问答题的输入框
        self.fill_answer_edit = QLineEdit()
        self.fill_answer_edit.setVisible(False)  # 初始时隐藏
        self.essay_answer_edit = PythonCodeEditor()
        self.essay_answer_edit.setVisible(False)  # 初始时隐藏

        question_layout.addWidget(self.question_type_label)
        question_layout.addWidget(self.question_text)
        question_layout.addLayout(self.options_layout)
        question_layout.addWidget(self.fill_answer_edit)
        question_layout.addWidget(self.essay_answer_edit)
        question_layout.addStretch()

        layout.addWidget(self.question_group)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.btn_prev = QPushButton("⬅️ 上一题")
        self.btn_prev.clicked.connect(self.prev_question)

        self.btn_next = QPushButton("➡️ 下一题")
        self.btn_next.clicked.connect(self.next_question)

        self.btn_submit = QPushButton("📝 交卷")
        self.btn_submit.clicked.connect(self.submit_exam)

        self.btn_back_exam = QPushButton("🔙 返回")
        self.btn_back_exam.clicked.connect(self.confirm_exit_exam)

        buttons = [self.btn_prev, self.btn_next, self.btn_submit, self.btn_back_exam]
        for btn in buttons:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        return page

    def create_result_page(self):
        """创建测验结果页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        title = QLabel("📊 测验结果")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 结果统计
        self.stats_group = QGroupBox("测验统计")
        stats_layout = QFormLayout(self.stats_group)

        self.total_score_label = QLabel()
        self.accuracy_label = QLabel()

        stats_layout.addRow("总分:", self.total_score_label)
        stats_layout.addRow("正确率:", self.accuracy_label)

        layout.addWidget(self.stats_group)

        # 错题按钮
        self.btn_wrong_answers = QPushButton("查看错题")
        self.btn_wrong_answers.setStyleSheet("background-color: #e74c3c;")
        self.btn_wrong_answers.clicked.connect(self.show_wrong_answers)
        layout.addWidget(self.btn_wrong_answers, alignment=Qt.AlignCenter)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.btn_retry = QPushButton("🔄 重新测验")
        self.btn_retry.clicked.connect(self.retry_exam)

        self.btn_back_result = QPushButton("🏠 返回主页")
        self.btn_back_result.clicked.connect(self.show_main_page)

        btn_layout.addWidget(self.btn_retry)
        btn_layout.addWidget(self.btn_back_result)

        layout.addLayout(btn_layout)

        return page

    def create_wrong_questions_page(self):
        """创建错题集页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        title = QLabel("❌ 错题集")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 题库选择
        bank_layout = QHBoxLayout()

        bank_layout.addWidget(QLabel("选择题库:"))

        self.wrong_bank_combo = QComboBox()
        self.wrong_bank_combo.currentIndexChanged.connect(self.update_wrong_list)
        bank_layout.addWidget(self.wrong_bank_combo)

        layout.addLayout(bank_layout)

        # 错题列表
        self.wrong_tree = QTreeWidget()
        self.wrong_tree.setHeaderLabels(["题型", "题目", "正确答案", "你的答案"])
        self.wrong_tree.setColumnWidth(0, 80)
        self.wrong_tree.setColumnWidth(1, 400)
        self.wrong_tree.setColumnWidth(2, 100)
        self.wrong_tree.setColumnWidth(3, 100)
        self.wrong_tree.setSelectionMode(QAbstractItemView.SingleSelection)

        # 设置行高
        row_height = 30  # 可以根据实际需求调整这个值
        self.wrong_tree.setStyleSheet(f"QTreeView::item {{ height: {row_height}px; }}")

        layout.addWidget(self.wrong_tree)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.btn_detail = QPushButton("🔍 查看详情")
        self.btn_detail.clicked.connect(self.show_wrong_detail)

        self.btn_delete_wrong = QPushButton("🗑️ 删除错题")
        self.btn_delete_wrong.clicked.connect(self.delete_wrong_question)

        self.btn_back_wrong = QPushButton("🔙 返回")
        self.btn_back_wrong.clicked.connect(self.back_from_wrong_page)

        buttons = [self.btn_detail, self.btn_delete_wrong, self.btn_back_wrong]
        for btn in buttons:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        return page

    def create_stats_page(self):
        """创建学习统计页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        title = QLabel("📊 学习统计")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 图表区域
        self.stats_canvas = FigureCanvas(plt.Figure(figsize=(10, 5)))
        layout.addWidget(self.stats_canvas)

        # 返回按钮
        self.btn_back_stats = QPushButton("🔙 返回")
        self.btn_back_stats.clicked.connect(self.show_main_page)
        layout.addWidget(self.btn_back_stats, alignment=Qt.AlignRight)

        return page

    def create_practice_setup_page(self):
        """创建刷题设置页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 标题
        title = QLabel("🌊 题海刷题模式")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 题库选择
        form_layout = QFormLayout()
        self.practice_bank_combo = QComboBox()
        form_layout.addRow("选择题库:", self.practice_bank_combo)

        # 刷题顺序选择
        self.order_combo = QComboBox()
        self.order_combo.addItems(["顺序", "逆序", "随机"])
        form_layout.addRow("刷题顺序:", self.order_combo)

        layout.addLayout(form_layout)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.btn_start_practice = QPushButton("开始刷题")
        self.btn_start_practice.clicked.connect(self.start_practice)

        self.btn_back_practice = QPushButton("返回")
        self.btn_back_practice.clicked.connect(self.show_main_page)

        btn_layout.addWidget(self.btn_start_practice)
        btn_layout.addWidget(self.btn_back_practice)

        layout.addLayout(btn_layout)

        return page

    def create_practice_page(self):
        """创建刷题页面"""
        page = QWidget()
        layout = QVBoxLayout(page)

        # 进度显示
        self.practice_progress_label = QLabel()
        self.practice_progress_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.practice_progress_label, alignment=Qt.AlignLeft)

        # 题目内容
        self.practice_question_group = QGroupBox()
        self.practice_question_group.setStyleSheet("QGroupBox { font-size: 14px; }")
        question_layout = QVBoxLayout(self.practice_question_group)

        self.practice_question_type_label = QLabel()
        self.practice_question_type_label.setStyleSheet("font-weight: bold; color: #3498db;")

        self.practice_question_text = QLabel()
        self.practice_question_text.setWordWrap(True)
        self.practice_question_text.setStyleSheet("font-size: 15px;")

        self.practice_options_layout = QVBoxLayout()

        question_layout.addWidget(self.practice_question_type_label)
        question_layout.addWidget(self.practice_question_text)
        question_layout.addLayout(self.practice_options_layout)
        question_layout.addStretch()

        layout.addWidget(self.practice_question_group)

        # 答案反馈
        self.answer_feedback = QLabel()
        self.answer_feedback.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.answer_feedback.setWordWrap(True)
        layout.addWidget(self.answer_feedback)

        # 按钮区域
        btn_layout = QHBoxLayout()

        self.btn_prev_practice = QPushButton("⬅️ 上一题")
        self.btn_prev_practice.clicked.connect(self.prev_practice_question)

        self.btn_next_practice = QPushButton("➡️ 下一题")
        self.btn_next_practice.clicked.connect(self.next_practice_question)

        self.btn_submit_practice = QPushButton("提交答案")
        self.btn_submit_practice.clicked.connect(self.submit_practice_answer)

        self.btn_back_practice_page = QPushButton("🔙 返回")
        self.btn_back_practice_page.clicked.connect(self.confirm_exit_practice)

        buttons = [self.btn_prev_practice, self.btn_next_practice,
                   self.btn_submit_practice, self.btn_back_practice_page]
        for btn in buttons:
            btn_layout.addWidget(btn)

        layout.addLayout(btn_layout)

        return page

    # 页面导航方法
    def show_main_page(self):
        """显示主页面"""
        self.content_area.setCurrentWidget(self.main_page)

    def show_bank_manager(self):
        """显示题库管理页面"""
        self.bank_list.clear()
        for bank_name in self.question_banks.keys():
            self.bank_list.addItem(bank_name)
        self.content_area.setCurrentWidget(self.bank_manager_page)

    def show_bank_editor(self, bank_name):
        """显示题库编辑器页面"""
        self.bank_editor_title.setText(f"✏️ 编辑题库: {bank_name}")
        self.current_question_bank = bank_name
        self.question_tree.clear()

        for question in self.question_banks[bank_name]:
            q_id = question.get('id')
            q_type = question['type']
            q_text = question['question']
            options = question.get('options', [])
            if options is None:
                options = []
            options = "\n".join(options) if options else ""
            answer = ", ".join(question['answer']) if isinstance(question['answer'], list) else question['answer']
            score = question.get('score', 1)

            item = QTreeWidgetItem(self.question_tree)
            item.setText(0, q_type)
            item.setText(1, q_text)
            item.setText(2, options)
            item.setText(3, answer)
            item.setText(4, str(score))
            item.setData(0, Qt.UserRole, q_id)

        self.content_area.setCurrentWidget(self.bank_editor_page)

    def show_exam_setup(self):
        """显示组卷设置页面"""
        self.bank_combo.clear()
        self.bank_combo.addItems(self.question_banks.keys())

        if self.current_question_bank and self.current_question_bank in self.question_banks:
            index = self.bank_combo.findText(self.current_question_bank)
            if index >= 0:
                self.bank_combo.setCurrentIndex(index)

        self.content_area.setCurrentWidget(self.exam_setup_page)

    def show_practice_setup(self):
        """显示刷题设置页面"""
        self.practice_bank_combo.clear()
        self.practice_bank_combo.addItems(self.question_banks.keys())
        self.content_area.setCurrentWidget(self.practice_setup_page)

    def show_question(self):
        """显示当前题目"""
        if not self.current_questions:
            QMessageBox.warning(self, "错误", "没有可用的题目!")
            return

        self.content_area.setCurrentWidget(self.exam_page)

        # 显示计时器
        self.timer_layout.parentWidget().show()
        self.update_exam_timer()

        # 更新进度
        self.progress_label.setText(f"题目 {self.current_index + 1}/{len(self.current_questions)}")

        # 获取当前题目
        current_question = self.current_questions[self.current_index]
        q_type = current_question['type']
        q_text = current_question['question']
        options = current_question.get('options', [])
        q_score = current_question.get('score', 1)

        # 显示题目信息
        self.question_type_label.setText(f"[{q_type}] (分值: {q_score})")
        self.question_text.setText(q_text)

        # 清除之前的选项
        while self.options_layout.count():
            child = self.options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 用户答案变量
        if q_type == "单选题":
            self.user_answer_rbs = []

            for i, option in enumerate(options):
                rb = QRadioButton(f"{chr(65 + i)}. {option}")
                if str(self.current_index) in self.user_answers:
                    if self.user_answers[str(self.current_index)] == chr(65 + i):
                        rb.setChecked(True)
                self.user_answer_rbs.append(rb)
                self.options_layout.addWidget(rb)

        elif q_type == "多选题":
            self.user_answer_cbs = []

            for i, option in enumerate(options):
                cb = QCheckBox(f"{chr(65 + i)}. {option}")
                if str(self.current_index) in self.user_answers:
                    if chr(65 + i) in self.user_answers[str(self.current_index)]:
                        cb.setChecked(True)
                self.user_answer_cbs.append(cb)
                self.options_layout.addWidget(cb)

        elif q_type == "判断题":
            self.user_answer_rbs = []

            rb_true = QRadioButton("正确")
            rb_false = QRadioButton("错误")

            if str(self.current_index) in self.user_answers:
                if self.user_answers[str(self.current_index)] == "正确":
                    rb_true.setChecked(True)
                else:
                    rb_false.setChecked(True)

            self.user_answer_rbs.append(rb_true)
            self.user_answer_rbs.append(rb_false)

            self.options_layout.addWidget(rb_true)
            self.options_layout.addWidget(rb_false)


        elif q_type == "填空题":
            # 创建填空题输入框
            self.fill_answer_edit = QLineEdit()
            if str(self.current_index) in self.user_answers:
                self.fill_answer_edit.setText(self.user_answers[str(self.current_index)])
            self.options_layout.addWidget(self.fill_answer_edit)

        elif q_type == "问答题":
            # 创建问答题输入框
            self.essay_answer_edit = PythonCodeEditor()
            if str(self.current_index) in self.user_answers:
                self.essay_answer_edit.setPlainText(self.user_answers[str(self.current_index)])
            self.options_layout.addWidget(self.essay_answer_edit)

        # 更新按钮状态
        self.btn_prev.setEnabled(self.current_index > 0)

        if self.current_index < len(self.current_questions) - 1:
            self.btn_next.show()
            self.btn_submit.hide()
        else:
            self.btn_next.hide()
            self.btn_submit.show()

    def show_practice_question(self):
        """显示刷题题目"""
        if not self.current_questions:
            QMessageBox.warning(self, "错误", "没有可用的题目!")
            return

        self.content_area.setCurrentWidget(self.practice_page)

        # 更新进度
        self.practice_progress_label.setText(f"题目 {self.current_index + 1}/{len(self.current_questions)}")
        self.answer_feedback.clear()

        # 获取当前题目
        current_question = self.current_questions[self.current_index]
        q_type = current_question['type']
        q_text = current_question['question']
        options = current_question.get('options', [])

        # 显示题目信息
        self.practice_question_type_label.setText(f"[{q_type}]")
        self.practice_question_text.setText(q_text)

        # 清除之前的选项
        while self.practice_options_layout.count():
            child = self.practice_options_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 用户答案变量
        if q_type == "单选题":
            self.user_answer_rbs = []

            for i, option in enumerate(options):
                rb = QRadioButton(f"{chr(65 + i)}. {option}")
                if str(self.current_index) in self.user_answers:
                    if self.user_answers[str(self.current_index)] == chr(65 + i):
                        rb.setChecked(True)
                self.user_answer_rbs.append(rb)
                self.practice_options_layout.addWidget(rb)

        elif q_type == "多选题":
            self.user_answer_cbs = []

            for i, option in enumerate(options):
                cb = QCheckBox(f"{chr(65 + i)}. {option}")
                if str(self.current_index) in self.user_answers:
                    if chr(65 + i) in self.user_answers[str(self.current_index)]:
                        cb.setChecked(True)
                self.user_answer_cbs.append(cb)
                self.practice_options_layout.addWidget(cb)

        elif q_type == "判断题":
            self.user_answer_rbs = []

            rb_true = QRadioButton("正确")
            rb_false = QRadioButton("错误")

            if str(self.current_index) in self.user_answers:
                if self.user_answers[str(self.current_index)] == "正确":
                    rb_true.setChecked(True)
                else:
                    rb_false.setChecked(True)

            self.user_answer_rbs.append(rb_true)
            self.user_answer_rbs.append(rb_false)

            self.practice_options_layout.addWidget(rb_true)
            self.practice_options_layout.addWidget(rb_false)

        elif q_type == "填空题":
            # 创建填空题输入框
            self.fill_answer_edit = QLineEdit()
            if str(self.current_index) in self.user_answers:
                self.fill_answer_edit.setText(self.user_answers[str(self.current_index)])
            self.practice_options_layout.addWidget(self.fill_answer_edit)

        elif q_type == "问答题":
            # 创建问答题输入框
            self.essay_answer_edit = PythonCodeEditor()
            if str(self.current_index) in self.user_answers:
                self.essay_answer_edit.setPlainText(self.user_answers[str(self.current_index)])
            self.practice_options_layout.addWidget(self.essay_answer_edit)

        # 更新按钮状态
        self.btn_prev_practice.setEnabled(self.current_index > 0)
        self.btn_next_practice.setEnabled(self.current_index < len(self.current_questions) - 1)
        self.btn_submit_practice.setEnabled(True)

    def show_exam_result(self, correct_count):
        """显示测验结果"""
        total_questions = len(self.current_questions)
        accuracy = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        self.total_score_label.setText(f"{self.score}/{self.total_score}")
        self.accuracy_label.setText(f"{accuracy:.1f}% ({correct_count}/{total_questions})")

        # 如果没有错题，隐藏查看错题按钮
        self.btn_wrong_answers.setVisible(correct_count < total_questions)

        self.content_area.setCurrentWidget(self.result_page)

    def show_wrong_questions(self):
        """显示错题集页面"""
        if not self.wrong_questions:
            sql = """select * from error_questions"""
            sql_class = """SELECT class FROM error_questions GROUP BY class;"""
            results_class = self.mysql_db.execute_many_or_loop(
                'error_questions',
                sql=sql_class,
                values=[],
                operation='query',
            )
            if results_class:
                for result in results_class:
                    if result['class']:
                        sql = "SELECT * FROM error_questions WHERE class = %s"
                        results_questions = self.mysql_db.execute_many_or_loop(
                            'error_questions',
                            sql=sql,
                            values=result['class'],
                            operation='query',
                        )
                        if result['class'] not in self.wrong_questions:
                            self.wrong_questions[result['class']] = []
                        if results_questions:
                            for result_new in results_questions:
                                if result_new['options']:
                                    result_new['options'] = json.loads(result_new['options'])
                                self.wrong_questions[result['class']].append(result_new)

        if not self.wrong_questions:
            QMessageBox.information(self, "提示", "错题集为空!")
            return

        self.wrong_bank_combo.clear()
        self.wrong_bank_combo.addItems(self.wrong_questions.keys())
        self.update_wrong_list()

        self.content_area.setCurrentWidget(self.wrong_questions_page)

        current_bank = self.wrong_bank_combo.currentText()
        if current_bank in self.wrong_questions:
            self.current_questions = self.wrong_questions[current_bank]
        self.content_area.setCurrentWidget(self.wrong_questions_page)

    def show_stats(self):
        """显示学习统计页面"""
        if not self.wrong_questions:
            QMessageBox.information(self, "提示", "暂无统计数据!")
            return

        # 创建图表
        fig = self.stats_canvas.figure
        fig.clear()

        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # 错题题型分布
        type_counts = {'填空题': 0, '问答题': 0, '单选题': 0, '多选题': 0, '判断题': 0}
        for bank_name, questions in self.wrong_questions.items():
            for question in questions:
                q_type = question['type']
                type_counts[q_type] += 1

        labels = list(type_counts.keys())
        sizes = list(type_counts.values())

        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax1.set_title('错题题型分布')

        # 各题库错题数量
        bank_names = list(self.wrong_questions.keys())
        wrong_counts = [len(questions) for questions in self.wrong_questions.values()]

        ax2.bar(bank_names, wrong_counts)
        ax2.set_title('各题库错题数量')
        ax2.set_ylabel('数量')
        ax2.tick_params(axis='x', rotation=45)

        fig.tight_layout()
        self.stats_canvas.draw()

        self.content_area.setCurrentWidget(self.stats_page)

    # 题库管理相关方法
    def import_question_bank(self):
        """导入题库文件"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "导入题库",
            "",
            "题库文件 (*.json *.xlsx)"
        )

        if not filename:
            return

        try:
            if filename.endswith('.json'):
                with open(filename, 'r', encoding='utf-8') as f:
                    bank_name = filename.split('/')[-1].replace('.json', '')
                    self.question_banks[bank_name] = json.load(f)
            elif filename.endswith('.xlsx'):
                bank_name = filename.split('/')[-1].replace('.xlsx', '')
                self.question_banks[bank_name] = self.load_excel_bank(filename)

            QMessageBox.information(self, "成功", f"题库 '{bank_name}' 导入成功!")
            self.show_bank_manager()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"导入失败: {str(e)}")

    def create_new_bank(self):
        """创建新题库"""
        bank_name, ok = QInputDialog.getText(self, "新建题库", "请输入题库名称:")
        if ok and bank_name:
            if bank_name in self.question_banks:
                QMessageBox.warning(self, "错误", "题库已存在!")
            else:
                self.question_banks[bank_name] = []
                self.bank_list.addItem(bank_name)
                QMessageBox.information(self, "成功", f"题库 '{bank_name}' 创建成功!")
                item = {'class': bank_name}
                self.mysql_db.insert('questions', data_dict=item, return_ids=True)

    def load_selected_bank(self):
        """加载选中的题库"""
        selected_items = self.bank_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "错误", "请先选择一个题库!")
            return

        bank_name = selected_items[0].text()
        self.current_question_bank = bank_name
        QMessageBox.information(self, "成功", f"题库 '{bank_name}' 已加载!")

    def edit_selected_bank(self):
        """编辑选中的题库"""
        selected_items = self.bank_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "错误", "请先选择一个题库!")
            return

        bank_name = selected_items[0].text()
        self.show_bank_editor(bank_name)

    def export_selected_bank(self):
        """导出选中的题库"""
        selected_items = self.bank_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "错误", "请先选择一个题库!")
            return

        bank_name = selected_items[0].text()

        # 选择导出格式
        formats = ["JSON (.json)", "Excel (.xlsx)"]
        format_choice, ok = QInputDialog.getItem(
            self, "选择导出格式", "请选择导出格式:", formats, 0, False
        )

        if ok:
            export_format = "json" if "JSON" in format_choice else "xlsx"
            self.save_question_bank(bank_name, export_format)

    def delete_selected_bank(self):
        """删除选中的题库"""
        selected_items = self.bank_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "错误", "请先选择一个题库!")
            return

        bank_name = selected_items[0].text()

        reply = QMessageBox.question(
            self,
            "确认",
            f"确定要删除题库 '{bank_name}' 吗?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # 从内存中删除
            del self.question_banks[bank_name]

            # 从列表框中删除
            self.bank_list.takeItem(self.bank_list.row(selected_items[0]))

            QMessageBox.information(self, "成功", f"题库 '{bank_name}' 已删除!")

    def add_question_dialog(self):
        """添加题目对话框"""
        if not self.current_question_bank:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("添加题目")
        dialog.setModal(True)
        dialog.resize(600, 500)

        layout = QVBoxLayout(dialog)

        # 题型选择
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("题型:"))

        q_type_combo = QComboBox()
        q_type_combo.addItems(["问答题", "填空题", "单选题", "多选题", "判断题"])
        type_layout.addWidget(q_type_combo)

        layout.addLayout(type_layout)

        # 题目内容
        layout.addWidget(QLabel("题目:"))

        # question_edit = QTextEdit()
        question_edit = QLineEdit()
        layout.addWidget(question_edit)

        # 选项框架
        options_group = QGroupBox("选项")
        options_layout = QVBoxLayout(options_group)

        self.option_edits = []
        for i in range(4):
            option_layout = QHBoxLayout()
            option_layout.addWidget(QLabel(f"选项 {chr(65 + i)}:"))

            option_edit = QLineEdit()
            self.option_edits.append(option_edit)
            option_layout.addWidget(option_edit)

            options_layout.addLayout(option_layout)

        layout.addWidget(options_group)

        # 答案框架
        answer_group = QGroupBox("答案")
        answer_layout = QVBoxLayout(answer_group)

        # 单选题答案
        self.single_answer_combo = QComboBox()
        self.single_answer_combo.addItems(["A", "B", "C", "D"])

        # 多选题答案
        self.multi_answer_checks = []
        multi_layout = QHBoxLayout()
        for i in range(4):
            cb = QCheckBox(chr(65 + i))
            self.multi_answer_checks.append(cb)
            multi_layout.addWidget(cb)

        # 判断题答案
        self.bool_answer_combo = QComboBox()
        self.bool_answer_combo.addItems(["正确", "错误"])

        # 填空题答案
        self.fill_answer_edit = QLineEdit()

        # 问答题答案
        self.essay_answer_edit = PythonCodeEditor()

        # 分值
        score_layout = QHBoxLayout()
        score_layout.addWidget(QLabel("分值:"))

        score_edit = QLineEdit("1")
        score_edit.setValidator(QIntValidator(1, 10))
        score_layout.addWidget(score_edit)

        layout.addWidget(answer_group)
        layout.addLayout(score_layout)

        # 按钮
        btn_layout = QHBoxLayout()

        add_btn = QPushButton("添加")
        add_btn.clicked.connect(lambda: self.add_question(
            dialog, q_type_combo, question_edit, score_edit
        ))

        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(dialog.reject)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

        # 题型变化事件
        def on_type_change(index):
            # 隐藏所有答案控件
            self.single_answer_combo.hide()
            for cb in self.multi_answer_checks:
                cb.hide()
            self.bool_answer_combo.hide()
            self.fill_answer_edit.hide()
            self.essay_answer_edit.hide()

            # 隐藏所有选项行
            for edit in self.option_edits:
                edit.hide()
                edit.parentWidget().hide()  # 更准确的隐藏父部件方式

            selected_type = q_type_combo.currentText()

            if selected_type == "单选题":
                self.single_answer_combo.show()
                # 显示前4个选项
                for i in range(4):
                    self.option_edits[i].show()
                    self.option_edits[i].parentWidget().show()
            elif selected_type == "多选题":
                for cb in self.multi_answer_checks:
                    cb.show()
                # 显示前4个选项
                for i in range(4):
                    self.option_edits[i].show()
                    self.option_edits[i].parentWidget().show()
            elif selected_type == "判断题":
                self.bool_answer_combo.show()
                # 只显示前2个选项（正确/错误）
                for i in range(2):
                    self.option_edits[i].show()
                    self.option_edits[i].parentWidget().show()
            elif selected_type == "填空题":
                self.fill_answer_edit.show()
                # 隐藏所有选项
                for edit in self.option_edits:
                    edit.hide()
                    edit.parentWidget().hide()
            elif selected_type == "问答题":
                self.essay_answer_edit.show()
                # 隐藏所有选项
                for edit in self.option_edits:
                    edit.hide()
                    edit.parentWidget().hide()

            # 先清空答案布局原有控件，避免重复添加
            while answer_layout.count():
                item = answer_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.setParent(None)

            # 根据题型重新添加对应答案控件到布局
            if selected_type == "单选题":
                answer_layout.addWidget(self.single_answer_combo)
            elif selected_type == "多选题":
                answer_layout.addLayout(multi_layout)
            elif selected_type == "判断题":
                answer_layout.addWidget(self.bool_answer_combo)
            elif selected_type == "填空题":
                answer_layout.addWidget(self.fill_answer_edit)
            elif selected_type == "问答题":
                answer_layout.addWidget(self.essay_answer_edit)

        q_type_combo.currentIndexChanged.connect(on_type_change)
        on_type_change(0)  # 初始化

        dialog.exec_()

    def add_question(self, dialog, q_type_combo, question_edit, score_edit):
        """添加题目到题库"""
        global answer
        q_type = q_type_combo.currentText()
        q_text = question_edit.text().strip()
        options = []

        # 处理选项逻辑
        if q_type in ["单选题", "多选题"]:
            for edit in self.option_edits[:4]:
                option = edit.text().strip()
                if option:
                    options.append(option)
        elif q_type == "判断题":
            options = ["正确", "错误"]
        # 填空题和问答题不需要选项
        elif q_type in ["填空题", "问答题"]:
            options = []  # 无选项

        # 验证题目和选项
        if not q_text:
            QMessageBox.warning(dialog, "错误", "题目不能为空!")
            return

        if q_type in ["单选题", "多选题"] and not options:
            QMessageBox.warning(dialog, "错误", "选择题至少需要一个选项!")
            return

        # 获取答案
        if q_type == "单选题":
            answer = self.single_answer_combo.currentText()
        elif q_type == "多选题":
            answer = []
            for i, cb in enumerate(self.multi_answer_checks):
                if cb.isChecked():
                    answer.append(chr(65 + i))
            answer = ", ".join(answer)
        elif q_type == "判断题":
            answer = self.bool_answer_combo.currentText()
        elif q_type == "填空题":
            answer = self.fill_answer_edit.text().strip()
        elif q_type == "问答题":
            answer = self.essay_answer_edit.toPlainText().strip()

        # 验证答案
        if not answer:
            QMessageBox.warning(dialog, "错误", "请设置正确答案!")
            return

        # 处理分值
        try:
            score = int(score_edit.text())
        except ValueError:
            score = 1

        if not options:
            options = None

        # 创建题目字典
        new_question = {
            'class': self.current_question_bank,
            'type': q_type,
            'question': q_text,
            'options': json.dumps(options),
            'answer': answer,
            'score': score
        }

        # 添加到题库
        if self.current_question_bank not in self.question_banks:
            self.question_banks[self.current_question_bank] = []
        self.question_banks[self.current_question_bank].append(new_question)

        # 更新树形视图
        item = QTreeWidgetItem(self.question_tree)
        item.setText(0, q_type)
        item.setText(1, q_text)
        item.setText(2, "\n".join(options) if options else "无选项")  # 填空题/问答题显示"无选项"
        item.setText(3, answer)
        item.setText(4, str(score))

        QMessageBox.information(dialog, "成功", "题目添加成功!")
        ids = self.mysql_db.insert('questions', data_dict=new_question, return_ids=True)
        if ids:
            # 获取插入记录的 id
            new_id = ids[0]
            # 将 id 添加到题目字典中
            new_question['id'] = new_id
            # 将 id 关联到 QTreeWidgetItem 上
            item.setData(0, Qt.UserRole, new_id)
        dialog.accept()

    def edit_question_dialog(self):
        """编辑题目对话框"""
        selected_items = self.question_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "错误", "请先选择要编辑的题目!")
            return

        item = selected_items[0]
        q_type = item.text(0)
        q_text = item.text(1)
        options = item.text(2).split("\n")
        if options == ["无选项"]:
            options = []
        answer = item.text(3)
        score = item.text(4)

        # 找到题库中的原始题目
        index = self.question_tree.indexOfTopLevelItem(item)
        original_question = self.question_banks[self.current_question_bank][index]

        dialog = QDialog(self)
        dialog.setWindowTitle("编辑题目")
        dialog.setModal(True)
        dialog.resize(600, 500)

        layout = QVBoxLayout(dialog)

        # 题型选择
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("题型:"))

        q_type_combo = QComboBox()
        q_type_combo.addItems(["单选题", "多选题", "判断题", "填空题", "问答题"])
        q_type_combo.setCurrentText(q_type)
        type_layout.addWidget(q_type_combo)

        layout.addLayout(type_layout)

        # 题目内容
        layout.addWidget(QLabel("题目:"))

        question_edit = QLineEdit()
        question_edit.setText(q_text)
        layout.addWidget(question_edit)

        # 选项框架
        options_group = QGroupBox("选项")
        options_layout = QVBoxLayout(options_group)

        self.option_edits = []
        for i in range(4):
            option_layout = QHBoxLayout()
            option_layout.addWidget(QLabel(f"选项 {chr(65 + i)}:"))

            option_edit = QLineEdit()
            if i < len(options):
                option_edit.setText(options[i])
            self.option_edits.append(option_edit)
            option_layout.addWidget(option_edit)

            options_layout.addLayout(option_layout)

        layout.addWidget(options_group)

        # 答案框架
        answer_group = QGroupBox("答案")
        answer_layout = QVBoxLayout(answer_group)

        # 单选题答案
        self.single_answer_combo = QComboBox()
        self.single_answer_combo.addItems(["A", "B", "C", "D"])

        # 多选题答案
        self.multi_answer_checks = []
        multi_layout = QHBoxLayout()
        for i in range(4):
            cb = QCheckBox(chr(65 + i))
            self.multi_answer_checks.append(cb)
            multi_layout.addWidget(cb)

        # 判断题答案
        self.bool_answer_combo = QComboBox()
        self.bool_answer_combo.addItems(["正确", "错误"])

        # 填空题答案
        self.fill_answer_edit = QLineEdit()

        # 问答题答案
        # self.essay_answer_edit = QTextEdit()
        self.essay_answer_edit = PythonCodeEditor()
        # self.essay_answer_edit = PythonCodeEditor(parent=dialog)  # 必须指定父控件
        # self.essay_answer_edit.setPlainText(answer)  # 设置文本
        # self.essay_answer_edit.refresh_code_blocks()  # 强制刷新代码块格式
        self.essay_answer_edit.setMaximumHeight(600)

        # 分值
        score_layout = QHBoxLayout()
        score_layout.addWidget(QLabel("分值:"))

        score_edit = QLineEdit(score)
        score_edit.setValidator(QtGui.QIntValidator(1, 10))
        score_layout.addWidget(score_edit)

        layout.addWidget(answer_group)
        layout.addLayout(score_layout)

        # 按钮
        btn_layout = QHBoxLayout()

        save_btn = QPushButton("保存")
        save_btn.clicked.connect(lambda: self.save_question_edit(
            dialog, q_type_combo, question_edit, score_edit, index
        ))

        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(dialog.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)

        # 题型变化事件
        def on_type_change(index):
            # 隐藏所有答案控件
            self.single_answer_combo.hide()
            for cb in self.multi_answer_checks:
                cb.hide()
            self.bool_answer_combo.hide()
            self.fill_answer_edit.hide()
            self.essay_answer_edit.hide()

            # 隐藏所有选项行
            for edit in self.option_edits:
                edit.hide()
                edit.parentWidget().hide()  # 更准确的隐藏父部件方式

            selected_type = q_type_combo.currentText()

            if selected_type == "单选题":
                self.single_answer_combo.show()
                # 显示前4个选项
                for i in range(4):
                    self.option_edits[i].show()
                    self.option_edits[i].parentWidget().show()
            elif selected_type == "多选题":
                for cb in self.multi_answer_checks:
                    cb.show()
                # 显示前4个选项
                for i in range(4):
                    self.option_edits[i].show()
                    self.option_edits[i].parentWidget().show()
            elif selected_type == "判断题":
                self.bool_answer_combo.show()
                # 只显示前2个选项（正确/错误）
                for i in range(2):
                    self.option_edits[i].show()
                    self.option_edits[i].parentWidget().show()
            elif selected_type == "填空题":
                self.fill_answer_edit.show()
                # 隐藏所有选项
                for edit in self.option_edits:
                    edit.hide()
                    edit.parentWidget().hide()
            elif selected_type == "问答题":
                self.essay_answer_edit.show()
                # 隐藏所有选项
                for edit in self.option_edits:
                    edit.hide()
                    edit.parentWidget().hide()

            # 先清空答案布局原有控件，避免重复添加
            while answer_layout.count():
                item = answer_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.setParent(None)

            # 根据题型重新添加对应答案控件到布局
            if selected_type == "单选题":
                answer_layout.addWidget(self.single_answer_combo)
            elif selected_type == "多选题":
                answer_layout.addLayout(multi_layout)
            elif selected_type == "判断题":
                answer_layout.addWidget(self.bool_answer_combo)
            elif selected_type == "填空题":
                answer_layout.addWidget(self.fill_answer_edit)
            elif selected_type == "问答题":
                answer_layout.addWidget(self.essay_answer_edit)

            # 设置当前答案
            if selected_type == "单选题":
                self.single_answer_combo.setCurrentText(answer)
            elif selected_type == "多选题":
                for char in answer.split(", "):
                    if char:
                        idx = ord(char.upper()) - ord('A')
                        if 0 <= idx < 4:
                            self.multi_answer_checks[idx].setChecked(True)
            elif selected_type == "判断题":
                self.bool_answer_combo.setCurrentText(answer)
            elif selected_type == "填空题":
                self.fill_answer_edit.setText(answer)
            elif selected_type == "问答题":
                self.essay_answer_edit.setText(answer)

        q_type_combo.currentIndexChanged.connect(on_type_change)
        on_type_change(q_type_combo.currentIndex())  # 初始化

        dialog.exec_()

    def save_question_edit(self, dialog, q_type_combo, question_edit, score_edit, index):
        """保存编辑后的题目"""
        global answer
        item = self.question_tree.topLevelItem(index)
        q_id = item.data(0, Qt.UserRole) if item else None
        q_type = q_type_combo.currentText()
        q_text = question_edit.toPlainText().strip()
        options = []

        # 处理选项逻辑
        if q_type in ["单选题", "多选题"]:
            for edit in self.option_edits[:4]:
                option = edit.text().strip()
                if option:
                    options.append(option)
        elif q_type == "判断题":
            options = ["正确", "错误"]
        # 填空题和问答题不需要选项
        elif q_type in ["填空题", "问答题"]:
            options = []  # 无选项

        # 验证题目和选项
        if not q_text:
            QMessageBox.warning(dialog, "错误", "题目不能为空!")
            return

        if q_type in ["单选题", "多选题"] and not options:
            QMessageBox.warning(dialog, "错误", "选择题至少需要一个选项!")
            return

        # 获取答案
        if q_type == "单选题":
            answer = self.single_answer_combo.currentText()
        elif q_type == "多选题":
            answer = []
            for i, cb in enumerate(self.multi_answer_checks):
                if cb.isChecked():
                    answer.append(chr(65 + i))
            answer = ", ".join(answer)
        elif q_type == "判断题":
            answer = self.bool_answer_combo.currentText()
        elif q_type == "填空题":
            answer = self.fill_answer_edit.text().strip()
        elif q_type == "问答题":
            answer = self.essay_answer_edit.toPlainText().strip()

        # 验证答案
        if not answer:
            QMessageBox.warning(dialog, "错误", "请设置正确答案!")
            return

        # 处理分值
        try:
            score = int(score_edit.text())
        except ValueError:
            score = 1

        if not options:
            options = None

        # 更新题目字典
        updated_question = {}
        updated_question['id'] = q_id
        updated_question['class'] = self.current_question_bank
        updated_question['type'] = q_type
        updated_question['question'] = q_text
        updated_question['options'] = json.dumps(options, ensure_ascii=False)
        updated_question['answer'] = answer
        updated_question['score'] = score

        # 更新题库
        self.question_banks[self.current_question_bank][index] = updated_question

        # 更新树形视图
        item = self.question_tree.topLevelItem(index)
        item.setText(0, q_type)
        item.setText(1, q_text)
        item.setText(2, "\n".join(options) if options else "无选项")  # 填空题/问答题显示"无选项"
        item.setText(3, answer)
        item.setText(4, str(score))

        # 更新数据库
        results_questions = self.mysql_db.update(
            'questions',
            condition={'id': int(q_id)},
            data_dict=updated_question
        )
        # 同步更新错题中的答案
        updated_question['question_id'] = int(q_id)
        updated_question.pop('id')
        results_questions = self.mysql_db.update(
            'error_questions',
            condition={'question_id': int(q_id)},
            data_dict=updated_question
        )
        QMessageBox.information(dialog, "成功", "题目更新成功!")

        dialog.accept()

    def delete_question(self):
        """删除题目"""
        selected_items = self.question_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "错误", "请先选择要删除的题目!")
            return

        reply = QMessageBox.question(
            self,
            "确认",
            "确定要删除选中的题目吗?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        # 从树形视图中删除
        index = self.question_tree.indexOfTopLevelItem(selected_items[0])
        self.question_tree.takeTopLevelItem(index)

        # 从题库中删除
        if index < len(self.question_banks[self.current_question_bank]):
            sql = """DELETE FROM questions WHERE id = %s """
            id = self.question_banks[self.current_question_bank][index]['id']
            values = (id,)
            results_questions = self.mysql_db.execute_many_or_loop(
                'questions',
                sql=sql,
                values=values,
                operation='delete',
            )

        QMessageBox.information(self, "成功", "题目已删除!")

    def save_question_bank(self, bank_name=None, export_format="json"):
        """保存题库到文件"""
        if not bank_name:
            bank_name = self.current_question_bank

        if export_format == "json":
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "保存题库",
                f"{bank_name}.json",
                "JSON 文件 (*.json)"
            )

            if filename:
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(self.question_banks[bank_name], f, ensure_ascii=False, indent=4)
                    QMessageBox.information(self, "成功", f"题库 '{bank_name}' 已保存为JSON格式!")
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"保存失败: {e}")
        else:  # Excel格式
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "导出题库",
                f"{bank_name}.xlsx",
                "Excel 文件 (*.xlsx)"
            )

            if filename:
                try:
                    self.export_to_excel(bank_name, filename)
                    QMessageBox.information(self, "成功", f"题库 '{bank_name}' 已导出为Excel格式!")
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"导出失败: {e}")

    def export_to_excel(self, bank_name, filename):
        """将题库导出为Excel文件"""
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "题库"

        # 写入表头
        headers = ["题型", "题目", "选项A", "选项B", "选项C", "选项D", "答案", "分值"]
        sheet.append(headers)

        # 写入题目
        for question in self.question_banks[bank_name]:
            row = [
                question["type"],
                question["question"]
            ]

            # 添加选项
            options = question.get("options", [])
            for i in range(4):
                row.append(options[i] if i < len(options) else "")

            # 添加答案和分值
            row.append(question["answer"])
            row.append(question.get("score", 1))

            sheet.append(row)

        workbook.save(filename)

    def load_question_bank_list(self):
        """加载题库列表"""
        sql = """select * from questions"""
        # 获取题目类型
        sql_class = """SELECT class FROM questions GROUP BY class;"""
        results_class = self.mysql_db.execute_many_or_loop(
            'questions',
            sql=sql_class,
            values=[],
            operation='query',
        )
        if results_class:
            for result in results_class:
                if result['class']:
                    sql = "SELECT * FROM questions WHERE class = %s"
                    results_questions = self.mysql_db.execute_many_or_loop(
                        'questions',
                        sql=sql,
                        values=result['class'],
                        operation='query',
                    )
                    if results_questions:
                        for result_new in results_questions:
                            if result_new['options']:
                                result_new['options'] = json.loads(result_new['options'])
                    # 将该类别的题目列表添加到字典中
                    self.question_banks[result['class']] = results_questions

    # 考试相关方法
    def start_exam(self):
        """开始考试"""
        bank_name = self.bank_combo.currentText()
        if not bank_name:
            QMessageBox.warning(self, "错误", "请选择题库!")
            return

        # 加载题库
        self.current_question_bank = bank_name
        questions = self.question_banks[bank_name]

        if not questions:
            QMessageBox.warning(self, "错误", "题库中没有题目!")
            return

        try:
            num_questions = int(self.num_questions.text())
            single_ratio = int(self.single_ratio.text())
            multi_ratio = int(self.multi_ratio.text())
            bool_ratio = int(self.bool_ratio.text())

            if single_ratio + multi_ratio + bool_ratio != 100:
                QMessageBox.warning(self, "错误", "题型比例总和必须为100%!")
                return
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的数字!")
            return

        # 按题型分类题目
        single_questions = [q for q in questions if q['type'] == "单选题"]
        multi_questions = [q for q in questions if q['type'] == "多选题"]
        bool_questions = [q for q in questions if q['type'] == "判断题"]

        # 计算各题型题目数量
        single_count = int(num_questions * single_ratio / 100)
        multi_count = int(num_questions * multi_ratio / 100)
        bool_count = num_questions - single_count - multi_count

        # 随机选择题目
        selected_questions = []

        if single_count > 0:
            if len(single_questions) >= single_count:
                selected_questions.extend(random.sample(single_questions, single_count))
            else:
                selected_questions.extend(single_questions)

        if multi_count > 0:
            if len(multi_questions) >= multi_count:
                selected_questions.extend(random.sample(multi_questions, multi_count))
            else:
                selected_questions.extend(multi_questions)

        if bool_count > 0:
            if len(bool_questions) >= bool_count:
                selected_questions.extend(random.sample(bool_questions, bool_count))
            else:
                selected_questions.extend(bool_questions)

        # 如果题目不足，补充随机题目
        if len(selected_questions) < num_questions:
            remaining = num_questions - len(selected_questions)
            all_questions = [q for q in questions if q not in selected_questions]
            if all_questions:
                selected_questions.extend(random.sample(all_questions, min(remaining, len(all_questions))))

        # 随机排序
        random.shuffle(selected_questions)

        # self.total_score = sum(q.get('score', 1) for q in selected_questions)
        self.total_score = sum(q.get('score') if q.get('score') is not None else 1 for q in selected_questions)

        # 设置考试计时器
        try:
            time_limit = int(self.time_limit.text())
            self.exam_mode = True
            self.exam_start_time = datetime.now()
            self.exam_time_limit = time_limit * 60  # 转换为秒
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的时间限制!")
            return

        # 设置当前题目
        self.current_questions = selected_questions
        self.current_index = 0
        self.user_answers = {}
        self.score = 0

        # 显示题目
        self.show_question()

    def update_exam_timer(self):
        """更新考试计时器"""
        if not self.exam_mode:
            return

        elapsed = (datetime.now() - self.exam_start_time).total_seconds()
        remaining = max(0, self.exam_time_limit - elapsed)

        minutes = int(remaining // 60)
        seconds = int(remaining % 60)

        self.timer_label.setText(f"剩余时间: {minutes:02d}:{seconds:02d}")

        if remaining <= 0:
            self.submit_exam()
        else:
            QTimer.singleShot(1000, self.update_exam_timer)

    def prev_question(self):
        """显示上一题"""
        self.save_current_answer()
        if self.current_index > 0:
            self.current_index -= 1
            self.show_question()

    def next_question(self):
        """显示下一题"""
        self.save_current_answer()
        if self.current_index < len(self.current_questions) - 1:
            self.current_index += 1
            self.show_question()
        else:
            self.submit_exam()

    def save_current_answer(self):
        """保存当前题目的答案"""
        current_question = self.current_questions[self.current_index]
        q_type = current_question['type']

        if q_type == "单选题":
            for i, rb in enumerate(self.user_answer_rbs):
                if rb.isChecked():
                    self.user_answers[str(self.current_index)] = chr(65 + i)
                    break
        elif q_type == "多选题":
            answer = []
            for i, cb in enumerate(self.user_answer_cbs):
                if cb.isChecked():
                    answer.append(chr(65 + i))
            if answer:
                self.user_answers[str(self.current_index)] = "".join(answer)
        elif q_type == "判断题":
            if self.user_answer_rbs[0].isChecked():
                self.user_answers[str(self.current_index)] = "正确"
            elif self.user_answer_rbs[1].isChecked():
                self.user_answers[str(self.current_index)] = "错误"
        elif q_type == "填空题":
            answer = self.fill_answer_edit.text().strip()
            if answer:
                self.user_answers[str(self.current_index)] = answer
        elif q_type == "问答题":
            answer = self.essay_answer_edit.toPlainText().strip()
            if answer:
                self.user_answers[str(self.current_index)] = answer

    def submit_exam(self):
        """提交试卷"""
        self.save_current_answer()
        self.exam_mode = False

        # 计算得分
        correct_count = 0
        self.score = 0

        for i, question in enumerate(self.current_questions):
            user_answer = self.user_answers.get(str(i), "")
            correct_answer = question['answer']
            q_score = question.get('score', 1)
            q_type = question['type']

            if q_type == "多选题":
                # 对多选题答案进行排序比较
                user_answer_sorted = "".join(sorted(user_answer.upper()))
                correct_answer_sorted = "".join(sorted(correct_answer.replace(", ", "").upper()))
                is_correct = user_answer_sorted == correct_answer_sorted
            elif q_type in ["填空题", "问答题"]:
                is_correct = str(user_answer).strip().upper() == str(correct_answer).strip().upper()
            else:
                is_correct = str(user_answer).upper() == str(correct_answer).upper()

            if is_correct:
                self.score += q_score
                correct_count += 1
            else:
                # 添加到错题集
                if self.current_question_bank not in self.wrong_questions:
                    self.wrong_questions[self.current_question_bank] = []

                wrong_question = question.copy()
                wrong_question['user_answer'] = user_answer
                wrong_question['question_index'] = i
                self.wrong_questions[self.current_question_bank].append(wrong_question)

                # 持久化到数据库
                wrong_question['question_id'] = wrong_question['id']
                wrong_question.pop('id')
                id = self.mysql_db.insert('error_questions', data_dict=wrong_question, return_ids=True)
                if id:
                    wrong_question['id'] = id[0]

        # 显示结果
        self.show_exam_result(correct_count)

    def retry_exam(self):
        """重新测验"""
        self.start_exam()

    def confirm_exit_exam(self):
        """确认退出考试"""
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要退出当前考试吗? 所有进度将丢失!",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.show_main_page()

    # 刷题相关方法
    def start_practice(self):
        """开始刷题"""
        bank_name = self.practice_bank_combo.currentText()
        if not bank_name:
            QMessageBox.warning(self, "错误", "请选择题库!")
            return

        # 加载题库
        self.current_question_bank = bank_name
        questions = self.question_banks[bank_name]

        if not questions:
            QMessageBox.warning(self, "错误", "题库中没有题目!")
            return

        # 设置刷题顺序
        self.practice_order = self.order_combo.currentText()

        # 准备题目
        self.current_questions = questions.copy()

        if self.practice_order == "逆序":
            self.current_questions.reverse()
        elif self.practice_order == "随机":
            random.shuffle(self.current_questions)

        self.current_index = 0
        self.user_answers = {}
        self.practice_mode = True

        # 显示第一题
        self.show_practice_question()

    def submit_practice_answer(self):
        """提交刷题答案"""
        self.save_current_practice_answer()
        current_question = self.current_questions[self.current_index]
        user_answer = self.user_answers.get(str(self.current_index), "")
        correct_answer = current_question['answer']

        # 检查答案
        if current_question['type'] == "多选题":
            # 对多选题答案进行排序比较
            user_answer_sorted = "".join(sorted(user_answer.upper()))
            correct_answer_sorted = "".join(sorted(correct_answer.replace(", ", "").upper()))
            is_correct = user_answer_sorted == correct_answer_sorted
        else:
            is_correct = str(user_answer).upper() == str(correct_answer).upper()

        # 显示反馈
        if is_correct:
            self.answer_feedback.setText("✅ 回答正确!")
            self.answer_feedback.setStyleSheet("color: green;")
        else:
            self.answer_feedback.setText(f"❌ 回答错误! 正确答案是: {correct_answer}")
            self.answer_feedback.setStyleSheet("color: red;")

            # 记录错题
            if self.current_question_bank not in self.wrong_questions:
                self.wrong_questions[self.current_question_bank] = []

            wrong_question = current_question.copy()
            wrong_question['user_answer'] = user_answer
            self.wrong_questions[self.current_question_bank].append(wrong_question)

        self.btn_submit_practice.setEnabled(False)

    def save_current_practice_answer(self):
        """保存当前刷题答案"""
        current_question = self.current_questions[self.current_index]
        q_type = current_question['type']

        if q_type == "单选题":
            for i, rb in enumerate(self.user_answer_rbs):
                if rb.isChecked():
                    self.user_answers[str(self.current_index)] = chr(65 + i)
                    break
        elif q_type == "多选题":
            answer = []
            for i, cb in enumerate(self.user_answer_cbs):
                if cb.isChecked():
                    answer.append(chr(65 + i))
            if answer:
                self.user_answers[str(self.current_index)] = "".join(answer)
        elif q_type == "判断题":
            if self.user_answer_rbs[0].isChecked():
                self.user_answers[str(self.current_index)] = "正确"
            elif self.user_answer_rbs[1].isChecked():
                self.user_answers[str(self.current_index)] = "错误"
        elif q_type == "填空题":
            # 获取填空题输入框的内容并保存
            answer = self.fill_answer_edit.text()
            if answer:
                self.user_answers[str(self.current_index)] = answer
        elif q_type == "问答题":
            # 获取问答题输入框的内容并保存
            answer = self.essay_answer_edit.toPlainText()
            if answer:
                self.user_answers[str(self.current_index)] = answer

    def prev_practice_question(self):
        """上一题"""
        if self.current_index > 0:
            self.current_index -= 1
            self.show_practice_question()

    def next_practice_question(self):
        """下一题"""
        if self.current_index < len(self.current_questions) - 1:
            self.current_index += 1
            self.show_practice_question()

    def confirm_exit_practice(self):
        """确认退出刷题"""
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要退出当前刷题吗?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.practice_mode = False
            self.show_main_page()

    # 错题集相关方法
    def show_wrong_answers(self):
        """显示错题"""
        self.show_wrong_questions()

    def update_wrong_list(self):
        """更新错题列表"""
        bank_name = self.wrong_bank_combo.currentText()
        if not bank_name:
            return

        # 清空树形视图
        self.wrong_tree.clear()

        # 加载错题
        for question in self.wrong_questions.get(bank_name, []):
            q_type = question['type']
            q_text = question['question']
            answer = question['answer']
            user_answer = question.get('user_answer', '')

            item = QTreeWidgetItem(self.wrong_tree)
            item.setText(0, q_type)
            item.setText(1, q_text)
            item.setText(2, answer)
            item.setText(3, user_answer)

    def show_wrong_detail(self):
        """显示错题详情"""
        selected_items = self.wrong_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "错误", "请先选择一道错题!")
            return

        item = selected_items[0]
        q_type = item.text(0)
        q_text = item.text(1)
        answer = item.text(2)
        user_answer = item.text(3)

        # 找到原始题目
        bank_name = self.wrong_bank_combo.currentText()
        index = None
        for q in self.wrong_questions.get(bank_name, []):
            if q['question'] == q_text and q['answer'] == answer and q.get('user_answer') == user_answer:
                index = q.get('question_index')
                break
        index = int(index)
        if index is None or index >= len(self.current_questions):
            QMessageBox.warning(self, "错误", "无法找到原始题目!")
            return

        original_question = self.current_questions[index]

        dialog = QDialog(self)
        dialog.setWindowTitle("错题详情")
        dialog.setModal(True)
        dialog.resize(800, 600)

        layout = QVBoxLayout(dialog)

        # 题目类型
        type_label = QLabel(f"[{q_type}]")
        type_label.setStyleSheet("font-weight: bold; color: #3498db;")
        layout.addWidget(type_label)

        # 题目文本
        question_label = QLabel(q_text)
        question_label.setWordWrap(True)
        question_label.setStyleSheet("font-size: 15px;")
        layout.addWidget(question_label)

        # 选项
        options_group = QGroupBox("选项")
        options_layout = QVBoxLayout(options_group)

        # 检查 options 是否为 None
        if original_question.get('options') is not None:
            for i, option in enumerate(original_question['options']):
                option_label = QLabel(f"{chr(65 + i)}. {option}")
                options_layout.addWidget(option_label)
        else:
            no_options_label = QLabel("无选项信息")
            options_layout.addWidget(no_options_label)

        layout.addWidget(options_group)

        # 正确答案
        correct_frame = QWidget()
        correct_layout = QHBoxLayout(correct_frame)

        correct_label = QLabel("正确答案:")
        correct_label.setStyleSheet("font-weight: bold; color: green;")

        answer_label = QLabel(answer)

        correct_layout.addWidget(correct_label)
        correct_layout.addWidget(answer_label)
        correct_layout.addStretch()

        layout.addWidget(correct_frame)

        # 你的答案
        user_frame = QWidget()
        user_layout = QHBoxLayout(user_frame)

        user_label = QLabel("你的答案:")
        user_label.setStyleSheet("font-weight: bold; color: red;")

        user_answer_label = QLabel(user_answer)

        user_layout.addWidget(user_label)
        user_layout.addWidget(user_answer_label)
        user_layout.addStretch()

        layout.addWidget(user_frame)

        # 解析(如果有)
        if 'explanation' in original_question:
            explanation_group = QGroupBox("解析")
            explanation_layout = QVBoxLayout(explanation_group)

            explanation_text = QTextEdit(original_question['explanation'])
            explanation_text.setReadOnly(True)
            explanation_layout.addWidget(explanation_text)

            layout.addWidget(explanation_group)

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)

        dialog.exec_()

    def delete_wrong_question(self):
        """删除错题"""
        selected_items = self.wrong_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "错误", "请先选择一道错题!")
            return

        bank_name = self.wrong_bank_combo.currentText()
        if not bank_name or bank_name not in self.wrong_questions:
            return

        reply = QMessageBox.question(
            self,
            "确认",
            "确定要删除这道错题吗?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        # 获取选中的错题信息
        item = selected_items[0]
        q_text = item.text(1)
        answer = item.text(2)
        user_answer = item.text(3)

        # 从错题集中删除
        for i, question in enumerate(self.wrong_questions[bank_name]):
            id = question.get('id')
            sql = """DELETE FROM error_questions WHERE id = %s """
            values = (id,)
            results_questions = self.mysql_db.execute_many_or_loop(
                'error_questions',
                sql=sql,
                values=values,
                operation='delete',
            )
            if question['question'] == q_text and question['answer'] == answer and question.get(
                    'user_answer') == user_answer:
                self.wrong_questions[bank_name].pop(i)
                break

        # 从树形视图中删除
        self.wrong_tree.takeTopLevelItem(self.wrong_tree.indexOfTopLevelItem(item))

        QMessageBox.information(self, "成功", "错题已删除!")

    def back_from_wrong_page(self):
        """从错题集页面返回"""
        if hasattr(self, 'from_result_page') and self.from_result_page:
            self.content_area.setCurrentWidget(self.result_page)
        else:
            self.show_main_page()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 设置全局字体
    font = QFont()
    font.setFamily("Arial")
    font.setPointSize(10)
    app.setFont(font)

    window = BrainyQuiz()
    window.show()
    sys.exit(app.exec_())
