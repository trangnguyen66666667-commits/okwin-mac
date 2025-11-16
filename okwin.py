from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os
import glob

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
    VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")
except Exception:
    from datetime import timezone, timedelta
    VN_TZ = timezone(timedelta(hours=7))

IMG_FOLDER = os.path.join(os.path.dirname(__file__), 'img')

class LogoButton(QtWidgets.QPushButton):
    """Custom QPushButton that scales a bit on hover for a nice effect."""
    def __init__(self, pixmap=None, label=None, parent=None):
        super().__init__(parent)
        self._pix = pixmap
        self._label = label or ''
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setFixedSize(280, 150)  # tăng kích thước logo
        self._anim = QtCore.QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(160)
        self._normal_geom = None
        self._hovered = False
        self.setStyleSheet('border:none; border-radius:14px; background-color:transparent;')
        if self._pix and not self._pix.isNull():
            icon = QtGui.QIcon(self._pix)
            self.setIcon(icon)
            self.setIconSize(self.size())
        else:
            self.setText(self._label)
            self.setStyleSheet(self.styleSheet() + ' font-weight:900; font-size:28px; color:white; background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #3a3a3a, stop:1 #242424);')

    def enterEvent(self, e):
        if not self._hovered:
            self._hovered = True
            g = self.geometry()
            self._normal_geom = g
            new = QtCore.QRect(g.x()-6, g.y()-6, int(g.width()*1.06), int(g.height()*1.06))
            self._anim.stop()
            self._anim.setStartValue(g)
            self._anim.setEndValue(new)
            self._anim.start()
        super().enterEvent(e)

    def leaveEvent(self, e):
        if self._hovered and self._normal_geom:
            self._hovered = False
            self._anim.stop()
            self._anim.setStartValue(self.geometry())
            self._anim.setEndValue(self._normal_geom)
            self._anim.start()
        super().leaveEvent(e)


class NameDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Liên Minh OKWIN")
        self.setModal(True)
        self.setFixedSize(420, 220)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Tên nhân viên")
        layout.addWidget(self.name_input)

        self.pass_input = QtWidgets.QLineEdit()
        self.pass_input.setPlaceholderText("Mật khẩu")
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.pass_input)

        btn_layout = QtWidgets.QHBoxLayout()
        ok_btn = QtWidgets.QPushButton("OK")
        cancel_btn = QtWidgets.QPushButton("Hủy")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        icon_path = resource_path("app4.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

    def getNameAndPassword(self):
        return self.name_input.text().strip(), self.pass_input.text().strip()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Liên Minh OK WIN')
        self.resize(1280, 760)
        # try to set app icon if exists in cwd
        ico = resource_path("app4.ico")
        if ico:
            self.setWindowIcon(QtGui.QIcon(ico))

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        main_layout = QtWidgets.QHBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)

        # left sidebar (fixed width, gray)
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setFixedWidth(170)
        self.sidebar.setStyleSheet('background:#6f6f6f;')
        s_layout = QtWidgets.QVBoxLayout(self.sidebar)
        s_layout.setContentsMargins(12,18,12,18)
        s_layout.setSpacing(12)

        self.btn_lien = QtWidgets.QPushButton('LIÊN MINH')
        self.btn_diem = QtWidgets.QPushButton('ĐIỂM RANH')
        self.btn_ok = QtWidgets.QPushButton('OKWIN')
        for w in (self.btn_lien, self.btn_diem, self.btn_ok):
            w.setMinimumHeight(60)
            w.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            w.setStyleSheet(self._sidebar_button_style(False))
            s_layout.addWidget(w)
        s_layout.addStretch()

        main_layout.addWidget(self.sidebar)

        # right area with gradient background
        self.right = QtWidgets.QFrame()
        self.right.setObjectName('rightArea')
        self.right.setStyleSheet('''
            QFrame#rightArea {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #0e1a35, stop:1 #0b1320);
            }
        ''')
        r_layout = QtWidgets.QVBoxLayout(self.right)
        r_layout.setContentsMargins(20,20,20,20)
        r_layout.setSpacing(10)

        # Title
        self.title_label = QtWidgets.QLabel()
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        logo_path = os.path.join(os.path.dirname(__file__), 'OKWIN11', 'OKWIN11.png')
        if os.path.exists(logo_path):
            pixmap = QtGui.QPixmap(logo_path)
            self.title_label.setPixmap(pixmap.scaledToHeight(90, QtCore.Qt.SmoothTransformation))
        r_layout.addWidget(self.title_label)
        img_path = os.path.join(IMG_FOLDER, 'OKWIN11.png')
        if os.path.exists(img_path):
            pixmap = QtGui.QPixmap(img_path)
            pixmap = QtGui.QPixmap(img_path)
            self.title_label.setPixmap(pixmap.scaledToHeight(150, QtCore.Qt.SmoothTransformation))
            self.title_label.setAlignment(QtCore.Qt.AlignCenter)
            r_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)
            self.title_label.setAlignment(QtCore.Qt.AlignCenter)
            r_layout.addWidget(self.title_label)
        else:
            r_layout.addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)

        # stacked pages
        self.pages = QtWidgets.QStackedWidget()
        r_layout.addWidget(self.pages)

        main_layout.addWidget(self.right)

        # Page 1 - logos grid
        page1 = QtWidgets.QWidget()
        p1_layout = QtWidgets.QVBoxLayout(page1)
        p1_layout.setAlignment(QtCore.Qt.AlignCenter)  # căn giữa toàn bộ logo

        # grid area with responsive behavior
        self.grid_widget = QtWidgets.QWidget()
        self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setHorizontalSpacing(36)
        self.grid_layout.setVerticalSpacing(30)
        self.grid_layout.setContentsMargins(60,40,60,40)
        self.grid_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.setContentsMargins(30,10,30,20)
        p1_layout.addWidget(self.grid_widget)
        p1_layout.addStretch()

        # Page 2 - Điểm Ranh
        page2 = QtWidgets.QWidget()
        p2_layout = QtWidgets.QVBoxLayout(page2)
        p2_layout.setAlignment(QtCore.Qt.AlignCenter)

        center_frame = QtWidgets.QFrame()
        center_frame.setStyleSheet('border:3px solid rgba(255,255,255,0.08); border-radius:18px; padding:40px;')
        center_layout = QtWidgets.QVBoxLayout(center_frame)
        center_layout.setAlignment(QtCore.Qt.AlignCenter)
        center_layout.setSpacing(20)

        self.date_label = QtWidgets.QLabel('')
        self.date_label.setAlignment(QtCore.Qt.AlignCenter)
        self.date_label.setStyleSheet('font-size:32px; font-weight:800; color:white;')
        center_layout.addWidget(self.date_label)

        self.time_label = QtWidgets.QLabel('')
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setStyleSheet('font-size:88px; font-weight:900; color:white;')
        center_layout.addWidget(self.time_label)

        self.name_title = QtWidgets.QLabel('TÊN NHÂN VIÊN')
        self.name_title.setAlignment(QtCore.Qt.AlignCenter)
        self.name_title.setStyleSheet('font-size:46px; font-weight:900; color:white;')
        center_layout.addWidget(self.name_title)

        self.preview_name = QtWidgets.QLabel('OKWIN')
        self.preview_name.setAlignment(QtCore.Qt.AlignCenter)
        self.preview_name.setStyleSheet('font-size:60px; font-weight:900; color:white;')
        center_layout.addWidget(self.preview_name)

        p2_layout.addStretch()
        p2_layout.addWidget(center_frame, alignment=QtCore.Qt.AlignCenter)
        p2_layout.addStretch()

        # Page 3 placeholder

        # Page 3 - Thông tin OKWIN
        page3 = QtWidgets.QWidget()
        p3_layout = QtWidgets.QVBoxLayout(page3)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)

        content_label = QtWidgets.QLabel()
        content_label.setStyleSheet("font-size:16px; color:white;")
        content_label.setWordWrap(True)
        content_label.setText("""
        <h2 style="color:white;">OKWIN là gì?</h2>
        <p><b>OKWIN liên minh</b> là một trong những tập đoàn giải trí có quy mô lớn hàng đầu tại Việt Nam, thu hút hàng triệu thành viên ghé đến mỗi ngày để tìm kiếm cơ hội đổi đời. Với sự kết hợp giữa công nghệ hiện đại và chăm sóc người dùng chuyên nghiệp, nền tảng tự tin mang đến những phút giây giải trí đặc sắc, tạo nên cộng đồng sôi động, nhiệt huyết và tích cực.</p>
        <p>Thương hiệu còn là địa điểm tích hợp rất nhiều cổng game đổi thưởng top đầu trên thị trường hiện nay bao gồm <b>Kuwin, 789win, 98win, King33, TG88, Vipwin</b> (tiền thân là Vin777), <b>LC88</b> gần đây chúng tôi vừa ra mắt thêm 2 thương hiệu mới đó là 32win và 789f. Điều này mang đến cho các dân chơi kho tàng game đa dạng, phong phú và chất lượng đỉnh cao. Đặc biệt là mỗi sảnh chơi đều có những nét đặc sắc riêng biệt, không bao giờ gây nhàm chán.</p>

        <h3 style="color:white;">Điểm danh các trang game lớn của tập đoàn Okwin</h3>
        <table border="1" cellpadding="6" cellspacing="0" style="color:white; border-collapse: collapse;">
        <thead>
        <tr>
        <th>Tên thương hiệu</th>
        <th>Thế mạnh</th>
        <th>Số lượng người chơi</th>
        </tr>
        </thead>
        <tbody>
        <tr><td>789win</td><td>Thành lập lâu đời, là thương hiệu phụ của 88online.</td><td>Hơn 500.000 người truy cập mỗi ngày</td></tr>
        <tr><td>Kuwin</td><td>Nổi bật với giao diện màu xanh dễ nhìn, chơi lâu không mỏi mắt</td><td>Hơn 500.000 người truy cập mỗi ngày</td></tr>
        <tr><td>98win</td><td>Nhiều trò chơi, tốc độ tải nhanh và ít bị nhà mạng chặn</td><td>Trên 300.000 người đăng nhập thường xuyên</td></tr>
        <tr><td>Vipwin</td><td>Có nhiều phần thưởng cho bản cá nhân, dễ nổ hũ</td><td>Số người nạp tiền lại lên đến 90%</td></tr>
        <tr><td>King33</td><td>Cổng game có thanh khoản nhanh nhất, nạp rút trong 3 phút</td><td>Đăng nhập hàng ngày 100.000 người</td></tr>
        <tr><td>32win</td><td>Cổng game công bằng, tỷ lệ trả thưởng cao hơn so với thị trường</td><td>Truy cập nhận thưởng 200.000 mỗi ngày</td></tr>
        <tr><td>789f</td><td>Sàn trực tiếp đá gà bóng đá sôi động</td><td>Đang cập nhật...</td></tr>
        <tr><td>UU88</td><td>Ứng dụng giới thiệu bạn bè tham gia ngay trên trang chủ, hoa hồng nhận liền tay</td><td>Đang cập nhật...</td></tr>
        <tr><td>Go8</td><td>Nền tảng game bài, casino, quay slot có bảo chứng</td><td>Đang cập nhật...</td></tr>
        </tbody>
        </table>

        <br><br>
        <h3 style="color:white;">THÔNG TIN LIÊN HỆ</h3>
        <ul>
        <li><b>Người đại diện:</b> Huỳnh Khải</li>
        <li><b>Website:</b> <a style="color:lightblue;" href="https://dennys.de.com/">https://dennys.de.com/</a></li>
        <li><b>Phone:</b> 0913261758</li>
        <li><b>Địa chỉ:</b> D3 Nam Kỳ Khởi Nghĩa, Phường Võ Thị Sáu, Quận 3, Hồ Chí Minh, Việt Nam</li>
        <li><b>Email:</b> contact@okwin88.com</li>
        </ul>
        """)
        scroll_layout.addWidget(content_label)
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)
        p3_layout.addWidget(scroll)


        # add pages
        self.pages.addWidget(page1)
        self.pages.addWidget(page2)
        self.pages.addWidget(page3)

        # connections
        self.btn_lien.clicked.connect(lambda: self.switch_tab(0, self.btn_lien))
        self.btn_diem.clicked.connect(lambda: self.switch_tab(1, self.btn_diem))
        self.btn_ok.clicked.connect(lambda: self.switch_tab(2, self.btn_ok))

        self._selected_btn = None
        self.switch_tab(0, self.btn_lien)

        # load logos from IMG_FOLDER
        self.logo_files = self._collect_logos()
        self._populate_logos()

        # clock
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update_clock)
        self.timer.start(1000)
        self._update_clock()

        # show name input dialog immediately after show
        QtCore.QTimer.singleShot(150, self._open_name_dialog_on_startup)

    def _find_icon(self):
        for p in os.listdir(os.path.dirname(__file__)):
            if p.lower().endswith('.ico'):
                return os.path.join(os.path.dirname(__file__), p)
        return None

    def _sidebar_button_style(self, active=False):
        if active:
            return ("background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #ffb000, stop:1 #ff9300); color:white; font-weight:900; font-size:18px; border-radius:8px;")
        return ("background: transparent; color: orange; font-weight:900; font-size:18px; border:none; text-align:left; padding-left:6px;")

    def switch_tab(self, index, btn):
        if self._selected_btn is not None:
            self._selected_btn.setStyleSheet(self._sidebar_button_style(False))
        btn.setStyleSheet(self._sidebar_button_style(True))
        self._selected_btn = btn
        self.pages.setCurrentIndex(index)

    def _collect_logos(self):
        # prefer certain filenames; fall back to any png/jpg/webp
        pref = ['98win.png','789f.png','789win.png','icon-go8.webp','icon-okfun.png','king33.png','kuwin.png','logo-32win.png','tg88.png','uu88.png','vipwin.png']
        files = {os.path.basename(f).lower(): f for f in glob.glob(os.path.join(IMG_FOLDER, '*'))}
        ordered = []
        for p in pref:
            if p in files:
                ordered.append(files[p])
        for k,v in files.items():
            if v not in ordered:
                ordered.append(v)
        return ordered

    def _populate_logos(self):
        # clear any existing
        for i in reversed(range(self.grid_layout.count())):
            w = self.grid_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
        cols = 4
        for idx, path in enumerate(self.logo_files):
            try:
                pix = QtGui.QPixmap(path).scaled(220,120, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
            except Exception:
                pix = QtGui.QPixmap()
            btn = LogoButton(pixmap=pix, label=os.path.splitext(os.path.basename(path))[0])
            # optional: connect a click to do something (e.g., print)
            btn.clicked.connect(lambda checked, p=path: print('Clicked', p))
            r = idx // cols
            c = idx % cols
            self.grid_layout.addWidget(btn, r, c)

        # Thêm label tên nhân viên ở cuối tab Liên Minh
        self.bottom_user_label = QtWidgets.QLabel()
        self.bottom_user_label.setStyleSheet("""
            color: white;
            font-size: 32px;
            font-weight: bold;
            padding: 20px 36px;
            border: 3px solid rgba(255, 255, 255, 0.25);
            border-radius: 16px;
            background-color: rgba(255,255,255,0.05);
        """)
        self.bottom_user_label.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.addWidget(self.bottom_user_label, 5, 0, 1, -1, alignment=QtCore.Qt.AlignCenter)


    def _update_clock(self):
        now = datetime.now(VN_TZ)
        current_time = now.strftime('%d/%m/%Y %H:%M:%S')
        if hasattr(self, 'bottom_user_label') and hasattr(self, 'preview_name'):
            self.bottom_user_label.setText(f"{self.preview_name.text()} - {current_time}")
            current_time = now.strftime("%d/%m/%Y %H:%M:%S")
            self.bottom_user_label.setText(f"{self.preview_name.text()} - {current_time}")
        now = datetime.now(VN_TZ)
        self.date_label.setText(f"NGÀY {now.day} THÁNG {now.month} NĂM {now.year}")
        self.time_label.setText(now.strftime('%H:%M:%S'))
  
    def _open_name_dialog_on_startup(self):
       correct_password = "okwin"
       while True:
           dlg = NameDialog(self)
           res = dlg.exec_()
           if res == QtWidgets.QDialog.Accepted:
               name, password = dlg.getNameAndPassword()
               if password != correct_password:
                   QtWidgets.QMessageBox.warning(self, "Sai mật khẩu", "Mật khẩu không đúng. Vui lòng thử lại.")
                   continue
               name = name.strip() or 'OK WIN'
               self.preview_name.setText(name.upper())
               now = datetime.now(VN_TZ).strftime('%d/%m/%Y %H:%M')
               self.bottom_user_label.setText(f'{name.upper()} - {now}')
               self.switch_tab(1, self.btn_diem)
               break
           else:
               QtWidgets.QApplication.quit()
               break

def main():
    app = QtWidgets.QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(__file__), "app4.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QtGui.QIcon(icon_path))
    # thêm dòng này
    app.setWindowIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "app4.ico")))

    pal = app.palette()
    pal.setColor(app.palette().Window, QtGui.QColor('#1f1f1f'))
    pal.setColor(app.palette().WindowText, QtGui.QColor('white'))
    app.setPalette(pal)

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()