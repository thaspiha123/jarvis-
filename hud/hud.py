import sys
import math

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QFont
from PySide6.QtWidgets import QApplication, QWidget


class JarvisHUD(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIS HUD")

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.showFullScreen()

        # -----------------------------------------------------
        # JARVIS STATE
        # -----------------------------------------------------

        self.state = "STANDBY"

        # -----------------------------------------------------
        # ANIMATION
        # -----------------------------------------------------

        self.outer_angle = 0
        self.middle_angle = 0
        self.inner_angle = 0
        self.pulse = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    # =========================================================
    # STATE
    # =========================================================

    def set_state(self, state):
        self.state = state.upper()
        self.update()

    # =========================================================
    # ANIMATION
    # =========================================================

    def animate(self):

        if self.state == "STANDBY":
            outer_speed = 0.20
            middle_speed = -0.35
            inner_speed = 0.55
            pulse_speed = 0.035

        elif self.state == "AWAKENING":
            outer_speed = 0.90
            middle_speed = -1.30
            inner_speed = 1.80
            pulse_speed = 0.14

        elif self.state == "LISTENING":
            outer_speed = 1.00
            middle_speed = -1.50
            inner_speed = 2.20
            pulse_speed = 0.18

        elif self.state == "PROCESSING":
            outer_speed = 1.60
            middle_speed = -2.20
            inner_speed = 3.00
            pulse_speed = 0.22

        elif self.state == "SPEAKING":
            outer_speed = 0.80
            middle_speed = -1.10
            inner_speed = 1.70
            pulse_speed = 0.15

        else:
            outer_speed = 0.30
            middle_speed = -0.50
            inner_speed = 0.70
            pulse_speed = 0.05

        self.outer_angle = (
            self.outer_angle + outer_speed
        ) % 360

        self.middle_angle = (
            self.middle_angle + middle_speed
        ) % 360

        self.inner_angle = (
            self.inner_angle + inner_speed
        ) % 360

        self.pulse += pulse_speed

        self.update()

    # =========================================================
    # GLOWING CIRCLE
    # =========================================================

    def glowing_circle(
        self,
        painter,
        x,
        y,
        radius
    ):

        if self.state == "STANDBY":
            glow_strength = 100

        elif self.state == "LISTENING":
            glow_strength = 180

        elif self.state == "PROCESSING":
            glow_strength = 210

        elif self.state == "SPEAKING":
            glow_strength = 190

        else:
            glow_strength = 150

        for glow in range(24, 0, -3):

            alpha = int(
                glow_strength * (24 - glow) / 24
            )

            pen = QPen(
                QColor(
                    0,
                    210,
                    255,
                    max(8, alpha)
                ),
                glow
            )

            painter.setPen(pen)

            painter.drawEllipse(
                x - radius,
                y - radius,
                radius * 2,
                radius * 2
            )

        painter.setPen(
            QPen(
                QColor(
                    80,
                    240,
                    255,
                    230
                ),
                2
            )
        )

        painter.drawEllipse(
            x - radius,
            y - radius,
            radius * 2,
            radius * 2
        )

    # =========================================================
    # TICKS
    # =========================================================

    def draw_ticks(
        self,
        painter,
        cx,
        cy,
        radius,
        count
    ):

        painter.save()

        painter.translate(cx, cy)

        for i in range(count):

            angle = (360 / count) * i

            radians = math.radians(angle)

            outer_x = math.cos(radians) * radius
            outer_y = math.sin(radians) * radius

            if i % 5 == 0:

                inner_radius = radius - 14
                width = 2

            else:

                inner_radius = radius - 6
                width = 1

            inner_x = math.cos(radians) * inner_radius
            inner_y = math.sin(radians) * inner_radius

            painter.setPen(
                QPen(
                    QColor(
                        70,
                        190,
                        230,
                        150
                    ),
                    width
                )
            )

            painter.drawLine(
                int(inner_x),
                int(inner_y),
                int(outer_x),
                int(outer_y)
            )

        painter.restore()

    # =========================================================
    # SEGMENTED RING
    # =========================================================

    def segmented_ring(
        self,
        painter,
        cx,
        cy,
        radius,
        segments,
        gap,
        angle
    ):

        painter.save()

        painter.translate(cx, cy)
        painter.rotate(angle)

        for i in range(segments):

            start = i * (360 / segments)

            if i % 4 == 0:

                pen = QPen(
                    QColor(
                        55,
                        220,
                        255,
                        220
                    ),
                    4
                )

            elif i % 2 == 0:

                pen = QPen(
                    QColor(
                        40,
                        180,
                        230,
                        150
                    ),
                    2
                )

            else:

                pen = QPen(
                    QColor(
                        30,
                        130,
                        190,
                        80
                    ),
                    1
                )

            painter.setPen(pen)

            span = (360 / segments) - gap

            painter.drawArc(
                -radius,
                -radius,
                radius * 2,
                radius * 2,
                int(start * 16),
                int(span * 16)
            )

        painter.restore()

    # =========================================================
    # MARKERS
    # =========================================================

    def draw_markers(
        self,
        painter,
        cx,
        cy,
        radius,
        count,
        angle
    ):

        painter.save()

        painter.translate(cx, cy)
        painter.rotate(angle)

        for i in range(count):

            if i % 4 != 0:
                continue

            a = math.radians(
                (360 / count) * i
            )

            x = math.cos(a) * radius
            y = math.sin(a) * radius

            painter.setPen(
                QPen(
                    QColor(
                        70,
                        220,
                        255,
                        190
                    ),
                    1
                )
            )

            painter.setBrush(
                QColor(
                    40,
                    180,
                    230,
                    100
                )
            )

            painter.drawRect(
                int(x - 3),
                int(y - 3),
                6,
                6
            )

        painter.restore()

    # =========================================================
    # SMALL RADIAL LINES
    # =========================================================

    def draw_radial_lines(
        self,
        painter,
        cx,
        cy,
        inner_radius,
        outer_radius,
        count,
        angle
    ):

        painter.save()

        painter.translate(cx, cy)
        painter.rotate(angle)

        for i in range(count):

            if i % 3 != 0:
                continue

            a = math.radians(
                (360 / count) * i
            )

            x1 = math.cos(a) * inner_radius
            y1 = math.sin(a) * inner_radius

            x2 = math.cos(a) * outer_radius
            y2 = math.sin(a) * outer_radius

            painter.setPen(
                QPen(
                    QColor(
                        50,
                        190,
                        240,
                        100
                    ),
                    1
                )
            )

            painter.drawLine(
                int(x1),
                int(y1),
                int(x2),
                int(y2)
            )

        painter.restore()

    # =========================================================
    # PAINT
    # =========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        width = self.width()
        height = self.height()

        cx = width // 2
        cy = height // 2

        # -----------------------------------------------------
        # BACKGROUND
        # -----------------------------------------------------

        painter.fillRect(
            self.rect(),
            QColor(
                2,
                8,
                18,
                255
            )
        )

        # -----------------------------------------------------
        # CORE SIZE
        # -----------------------------------------------------

        if self.state == "STANDBY":

            pulse_amount = 4

        elif self.state == "LISTENING":

            pulse_amount = 13

        elif self.state == "PROCESSING":

            pulse_amount = 17

        elif self.state == "SPEAKING":

            pulse_amount = 11

        else:

            pulse_amount = 8

        pulse_radius = (
            72 +
            int(
                math.sin(self.pulse) *
                pulse_amount
            )
        )

        # -----------------------------------------------------
        # OUTER RINGS
        # -----------------------------------------------------

        for radius in [300, 315, 330]:

            painter.setPen(
                QPen(
                    QColor(
                        50,
                        170,
                        220,
                        90
                    ),
                    1
                )
            )

            painter.drawEllipse(
                cx - radius,
                cy - radius,
                radius * 2,
                radius * 2
            )

        # -----------------------------------------------------
        # OUTER SEGMENTS
        # -----------------------------------------------------

        self.segmented_ring(
            painter,
            cx,
            cy,
            320,
            56,
            3,
            self.outer_angle
        )

        # -----------------------------------------------------
        # OUTER TICKS
        # -----------------------------------------------------

        self.draw_ticks(
            painter,
            cx,
            cy,
            310,
            144
        )

        # -----------------------------------------------------
        # RADIAL TECHNICAL LINES
        # -----------------------------------------------------

        self.draw_radial_lines(
            painter,
            cx,
            cy,
            260,
            295,
            72,
            self.outer_angle
        )

        # -----------------------------------------------------
        # MIDDLE RINGS
        # -----------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    40,
                    180,
                    230,
                    130
                ),
                1
            )
        )

        for radius in [235, 250, 265]:

            painter.drawEllipse(
                cx - radius,
                cy - radius,
                radius * 2,
                radius * 2
            )

        # -----------------------------------------------------
        # MIDDLE SEGMENTS
        # -----------------------------------------------------

        self.segmented_ring(
            painter,
            cx,
            cy,
            245,
            40,
            5,
            self.middle_angle
        )

        # -----------------------------------------------------
        # MARKERS
        # -----------------------------------------------------

        self.draw_markers(
            painter,
            cx,
            cy,
            215,
            56,
            self.middle_angle
        )

        # -----------------------------------------------------
        # INNER TECHNICAL RINGS
        # -----------------------------------------------------

        self.segmented_ring(
            painter,
            cx,
            cy,
            175,
            36,
            5,
            self.inner_angle
        )

        painter.setPen(
            QPen(
                QColor(
                    60,
                    210,
                    245,
                    150
                ),
                1
            )
        )

        painter.drawEllipse(
            cx - 185,
            cy - 185,
            370,
            370
        )

        # -----------------------------------------------------
        # INNER TICKS
        # -----------------------------------------------------

        self.draw_ticks(
            painter,
            cx,
            cy,
            160,
            96
        )

        # -----------------------------------------------------
        # CENTRAL GLOW
        # -----------------------------------------------------

        self.glowing_circle(
            painter,
            cx,
            cy,
            pulse_radius
        )

        # -----------------------------------------------------
        # INNER CORE RINGS
        # -----------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    90,
                    245,
                    255,
                    230
                ),
                3
            )
        )

        painter.drawEllipse(
            cx - 105,
            cy - 105,
            210,
            210
        )

        painter.setPen(
            QPen(
                QColor(
                    40,
                    220,
                    255,
                    130
                ),
                6
            )
        )

        painter.drawEllipse(
            cx - 88,
            cy - 88,
            176,
            176
        )

        # -----------------------------------------------------
        # CENTER
        # -----------------------------------------------------

        painter.setPen(
            QPen(
                QColor(
                    100,
                    245,
                    255,
                    230
                ),
                2
            )
        )

        painter.setBrush(
            QColor(
                0,
                40,
                65,
                170
            )
        )

        painter.drawEllipse(
            cx - 68,
            cy - 68,
            136,
            136
        )

        # -----------------------------------------------------
        # CENTER DOT
        # -----------------------------------------------------

        center_size = 5

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QColor(
                80,
                240,
                255,
                240
            )
        )

        painter.drawEllipse(
            cx - center_size,
            cy - center_size,
            center_size * 2,
            center_size * 2
        )

        # -----------------------------------------------------
        # TOP TITLE
        # -----------------------------------------------------

        painter.setPen(
            QColor(
                110,
                220,
                255,
                220
            )
        )

        painter.setFont(
            QFont(
                "Consolas",
                18,
                QFont.Weight.Light
            )
        )

        painter.drawText(
            0,
            40,
            width,
            30,
            Qt.AlignmentFlag.AlignCenter,
            "J A R V I S"
        )

        # -----------------------------------------------------
        # LEFT INFORMATION
        # -----------------------------------------------------

        painter.setFont(
            QFont(
                "Consolas",
                11
            )
        )

        painter.setPen(
            QColor(
                70,
                190,
                230,
                180
            )
        )

        painter.drawText(
            40,
            50,
            "SYSTEM // ONLINE"
        )

        painter.drawText(
            40,
            72,
            "CORE // ACTIVE"
        )

        painter.drawText(
            40,
            94,
            "VOICE // READY"
        )

        # -----------------------------------------------------
        # RIGHT INFORMATION
        # -----------------------------------------------------

        painter.drawText(
            width - 180,
            50,
            "AI CORE"
        )

        painter.drawText(
            width - 180,
            72,
            f"MODE // {self.state}"
        )

        painter.drawText(
            width - 180,
            94,
            "LINK // ACTIVE"
        )

        # -----------------------------------------------------
        # BOTTOM STATUS
        # -----------------------------------------------------

        painter.setPen(
            QColor(
                80,
                210,
                245,
                190
            )
        )

        painter.setFont(
            QFont(
                "Consolas",
                12
            )
        )

        painter.drawText(
            0,
            height - 75,
            width,
            25,
            Qt.AlignmentFlag.AlignCenter,
            self.state
        )

        painter.setFont(
            QFont(
                "Consolas",
                10
            )
        )

        if self.state == "STANDBY":

            message = "DOUBLE CLAP TO ACTIVATE"

        elif self.state == "AWAKENING":

            message = "INITIALIZING JARVIS CORE"

        elif self.state == "LISTENING":

            message = "LISTENING FOR COMMAND"

        elif self.state == "PROCESSING":

            message = "PROCESSING REQUEST"

        elif self.state == "SPEAKING":

            message = "JARVIS RESPONSE"

        else:

            message = "SYSTEM READY"

        painter.drawText(
            0,
            height - 45,
            width,
            25,
            Qt.AlignmentFlag.AlignCenter,
            message
        )

        # -----------------------------------------------------
        # ESC EXIT
        # -----------------------------------------------------

        painter.setPen(
            QColor(
                70,
                150,
                190,
                120
            )
        )

        painter.drawText(
            width - 180,
            height - 35,
            150,
            20,
            Qt.AlignmentFlag.AlignRight,
            "ESC  EXIT"
        )

    # =========================================================
    # ESCAPE
    # =========================================================

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_Escape:
            self.close()


# =============================================================
# START HUD
# =============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    hud = JarvisHUD()
    hud.show()

    sys.exit(app.exec())