import sys
import os

from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QLineEdit,
    QMainWindow,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QSlider)

class Paths:
    base = os.path.dirname('/Users/zohaibsuhail/Documents/Coding/Application Creating/Browser/')
    icons = os.path.join(base,'/Users/zohaibsuhail/Documents/Coding/Application Creating/Browser/icons')
    
    @classmethod
    def icon(cls,filename):
        return os.path.join(cls.icons,filename)
    
class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        QBtn = QDialogButtonBox.StandardButton.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Zib Browser")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(Paths.icon("za-icon-128.png")))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 01.00"))
        layout.addWidget(QLabel("Copyright 2023 Suhail Inc."))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        
        navtb = QToolBar('Zib Bar')
        navtb.setIconSize(QSize(24,24))
        self.addToolBar(navtb)
        
        back_btn = QAction(QIcon(Paths.icon("arrow-180.png")), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)
        
        next_btn = QAction(QIcon(Paths.icon("arrow-000.png")), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(Paths.icon("arrow-circle-315.png")),"Reload",self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
        
        home_btn = QAction(QIcon(Paths.icon("home.png")), "Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()
        
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(Paths.icon("lock-nossl.png")))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)
        
        stop_btn = QAction(QIcon(Paths.icon("cross-circle.png")), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        self.menuBar().setNativeMenuBar(False)
        self.statusBar()

        file_menu = self.menuBar().addMenu("&File")
        
        new_tab_action = QAction(
            QIcon(Paths.icon("ui-tab--plus.png")),
            "New Tab",
            self,
        )
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(Paths.icon("disk--arrow.png")),"Open file...",self,)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(Paths.icon("disk--pencil.png")),"Save Page As...",self,)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)
        
        print_action = QAction(QIcon(Paths.icon("printer.png")), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)
        self.printer = QPrinter()

        help_menu = self.menuBar().addMenu("&Help")
        
        about_action = QAction(QIcon(Paths.icon("question.png")),"About Zib Browser",self,)
        about_action.setStatusTip("Find out more about Zib Browser")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        navigate_zib_action = QAction(QIcon(Paths.icon("lifebuoy.png")),"Zib Browser Homepage",self)
        navigate_zib_action.setStatusTip("Go to Python GUIs Infor")
        navigate_zib_action.triggered.connect(self.navigate_zib)
        help_menu.addAction(navigate_zib_action)
        
        self.add_new_tab(QUrl("https://www.linkedin.com/in/zohaib-suhail/"), "Homepage")
        self.show()
        self.setWindowTitle("Zib Browser")
        self.setWindowIcon(QIcon(Paths.icon("za-icon-64.png")))
        
        
        self.zoomInAction = QAction("Zoom In", self)
        self.zoomInAction.setShortcut("Ctrl++")
        self.zoomInAction.triggered.connect(self.zoomIn)

        self.zoomOutAction = QAction("Zoom Out", self)
        self.zoomOutAction.setShortcut("Ctrl+-")
        self.zoomOutAction.triggered.connect(self.zoomOut)

        self.addAction(self.zoomInAction)
        self.addAction(self.zoomOutAction)
        
    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl("")
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))
    
    def tab_open_doubleclick(self, i):
        if i == -1: 
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("%s - Zib Browser" % title)
        
    def navigate_zib(self):
        self.tabs.currentWidget().setUrl(QUrl("https://academy.pythonguis.com/"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self,
            "Open file",
            "",
            "Hypertext Markup Language (*.htm *.html);;"
            "All files (*.*)")
        if filename:
            with open(filename, "r") as f:
                html = f.read()
            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self,
            "Save Page As",
            "",
            "Hypertext Markup Language (*.htm *html);;"
            "All files (*.*)")
        if filename:
            def writer(html):
                with open(filename, "w") as f:
                    f.write(html)
            self.tabs.currentWidget().page().toHtml(writer)
            
    def print_page(self):
        page = self.tabs.currentWidget().page()
        def callback(*args):
            pass
        dlg = QPrintDialog(self.printer)
        dlg.accepted.connect(callback)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            page.print(self.printer, callback)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.linkedin.com/in/zohaib-suhail"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        if q.scheme() == "https":
            self.httpsicon.setPixmap(QPixmap(Paths.icon("lock-ssl.png")))
        else:
            self.httpsicon.setPixmap(QPixmap(Paths.icon("lock-nossl.png")))
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        
    def zoomIn(self):
        zoomFactor = self.view.zoomFactor()
        self.view.setZoomFactor(zoomFactor + 0.1)

    def zoomOut(self):
        zoomFactor = self.view.zoomFactor()
        self.view.setZoomFactor(zoomFactor - 0.1)

                           
app = QApplication(sys.argv)
app.setApplicationName("Zib Browser")
app.setOrganizationName("Suhail")
app.setOrganizationDomain("zib.org")

window = MainWindow()

app.exec()