import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton,QGroupBox
from PyQt5.QtGui import QDoubleValidator
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import array
import numpy as np
from pathlib import Path
from .camera import *
from .object import *
from .draw import *
from .transformations import *

# Defining the relative path of the object
PROJECT_ROOT = Path(__file__).resolve().parents[1]
OBJECT_NAME = "bulbasaur" # Edit here to replace the object
OBJECT_STL_PATH = PROJECT_ROOT / "assets" / "models" / f"{OBJECT_NAME}.stl"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_variables()
        self.setWindowTitle("Grid Layout")
        self.setGeometry(100, 100,1280 , 720)
        self.setup_ui()

    def set_variables(self):
        self.objeto_original, self.vectors, self.stl_mesh = load_object(stl_path=OBJECT_STL_PATH)
        self.objeto = self.objeto_original.copy()
        self.world = np.eye(4)
        self.cam_original = move(5, 0, 0)@z_rotation(90)@x_rotation(-90)
        self.cam = self.cam_original.copy()
        self.cam_obj = np.linalg.inv(self.cam)@self.objeto
        self.px_base = 1280
        self.px_altura = 720
        self.dist_foc = 30
        self.stheta = 0
        self.ox = self.px_base/2
        self.oy = self.px_altura/2
        self.ccd = [36,24]
        self.projection_matrix = self.generate_intrinsic_params_matrix()
        
    def setup_ui(self):
        # Criar o layout de grade
        grid_layout = QGridLayout()

        # Criar os widgets
        line_edit_widget1 = self.create_world_widget("Ref mundo")
        line_edit_widget2  = self.create_cam_widget("Ref camera")
        line_edit_widget3  = self.create_intrinsic_widget("params instr")

        self.canvas = self.create_matplotlib_canvas()

        # Adicionar os widgets ao layout de grade
        grid_layout.addWidget(line_edit_widget1, 0, 0)
        grid_layout.addWidget(line_edit_widget2, 0, 1)
        grid_layout.addWidget(line_edit_widget3, 0, 2)
        grid_layout.addWidget(self.canvas, 1, 0, 1, 3)

        # Criar um widget para agrupar o botão de reset
        reset_widget = QWidget()
        reset_layout = QHBoxLayout()
        reset_widget.setLayout(reset_layout)

        # Criar o botão de reset vermelho
        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(50, 30)  # Define um tamanho fixo para o botão (largura: 50 pixels, altura: 30 pixels)
        style_sheet = """
            QPushButton {
                color : white ;
                background: rgba(255, 127, 130,128);
                font: inherit;
                border-radius: 5px;
                line-height: 1;
            }
        """
        reset_button.setStyleSheet(style_sheet)
        reset_button.clicked.connect(self.reset_canvas)

        # Adicionar o botão de reset ao layout
        reset_layout.addWidget(reset_button)

        # Adicionar o widget de reset ao layout de grade
        grid_layout.addWidget(reset_widget, 2, 0, 1, 3)

        # Criar um widget central e definir o layout de grade como seu layout
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        
        # Definir o widget central na janela principal
        self.setCentralWidget(central_widget)

    def create_intrinsic_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['n_pixels_base:', 'n_pixels_altura:', 'ccd_x:', 'ccd_y:', 'dist_focal:', 'sθ:']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")
 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_params_intrinsc(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget
    
    def create_world_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_world ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_world(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_cam_widget(self, title):
        # Criar um widget para agrupar os QLineEdit
        line_edit_widget = QGroupBox(title)
        line_edit_layout = QVBoxLayout()
        line_edit_widget.setLayout(line_edit_layout)

        # Criar um layout de grade para dividir os QLineEdit em 3 colunas
        grid_layout = QGridLayout()

        line_edits = []
        labels = ['X(move):', 'X(angle):', 'Y(move):', 'Y(angle):', 'Z(move):', 'Z(angle):']  # Texto a ser exibido antes de cada QLineEdit

        # Adicionar widgets QLineEdit com caixa de texto ao layout de grade
        for i in range(1, 7):
            line_edit = QLineEdit()
            label = QLabel(labels[i-1])
            validator = QDoubleValidator()  # Validador numérico
            line_edit.setValidator(validator)  # Aplicar o validador ao QLineEdit
            grid_layout.addWidget(label, (i-1)//2, 2*((i-1)%2))
            grid_layout.addWidget(line_edit, (i-1)//2, 2*((i-1)%2) + 1)
            line_edits.append(line_edit)

        # Criar o botão de atualização
        update_button = QPushButton("Atualizar")

        ##### Você deverá criar, no espaço reservado ao final, a função self.update_cam ou outra que você queira 
        # Conectar a função de atualização aos sinais de clique do botão
        update_button.clicked.connect(lambda: self.update_cam(line_edits))

        # Adicionar os widgets ao layout do widget line_edit_widget
        line_edit_layout.addLayout(grid_layout)
        line_edit_layout.addWidget(update_button)

        # Retornar o widget e a lista de caixas de texto
        return line_edit_widget

    def create_matplotlib_canvas(self):
        # Criar um widget para exibir os gráficos do Matplotlib
        canvas_widget = QWidget()
        canvas_layout = QHBoxLayout()
        canvas_widget.setLayout(canvas_layout)

        # Criar um objeto FigureCanvas para exibir o gráfico 2D
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_title("Imagem")
        self.canvas1 = FigureCanvas(self.fig1)

        ##### Falta acertar os limites do eixo X
        self.ax1.set_xlim([0,self.px_base])
        ##### Falta acertar os limites do eixo Y
        self.ax1.set_ylim([self.px_altura,0])

        ##### Você deverá criar a função de projeção 
        object_2d = self.projection_2d()

        ##### Falta plotar o object_2d que retornou da projeção
        self.ax1.plot(object_2d[0,:],object_2d[1,:])
          
        self.ax1.grid('True')
        self.ax1.set_aspect('equal')  
        canvas_layout.addWidget(self.canvas1)

        # Criar um objeto FigureCanvas para exibir o gráfico 3D
        self.fig2 = plt.figure()
        self.ax2 = self.fig2.add_subplot(111, projection='3d')
        set_plot(self.ax2, self.fig2, lim=[-5,5])

        ##### Falta plotar o seu objeto 3D e os referenciais da câmera e do mundo
        
        self.ax2 = draw_arrows(self.world[:,-1],self.world[:,0:3],self.ax2,3)
        self.ax2 = draw_arrows(self.cam[:,-1],self.cam[:,0:3],self.ax2,1)
        self.ax2.plot(self.objeto[0,:],self.objeto[1,:],self.objeto[2,:],'r')
        
        self.canvas2 = FigureCanvas(self.fig2)
        canvas_layout.addWidget(self.canvas2)

        # Retornar o widget de canvas
        return canvas_widget


    ##### Você deverá criar as suas funções aqui
    
    def update_params_intrinsc(self, line_edits):
        params = [
            self.px_base,
            self.px_altura,
            self.ccd[0],
            self.ccd[1],
            self.dist_foc,
            self.stheta,
        ]

        for index, line_edit in enumerate(line_edits):
            text = line_edit.text().strip().replace(",", ".")
            if text:
                params[index] = float(text)

        self.px_base = params[0]
        self.px_altura = params[1]
        self.ccd = [params[2], params[3]]
        self.dist_foc = params[4]
        self.stheta = params[5]
        self.ox = self.px_base / 2
        self.oy = self.px_altura / 2
        self.projection_matrix = self.generate_intrinsic_params_matrix()
        self.update_canvas()

    def read_transform_values(self, line_edits):
        values = []

        for line_edit in line_edits:
            text = line_edit.text().strip().replace(",", ".")
            values.append(float(text) if text else 0)

        return values

    def update_world(self,line_edits):
        values = self.read_transform_values(line_edits)

        T = move(values[0], values[2], values[4])
        Rx = x_rotation(values[1])
        Ry = y_rotation(values[3])
        Rz = z_rotation(values[5])
        R = Rz @ Ry @ Rx

        self.cam[0:3, 0:3] = R[0:3, 0:3] @ self.cam[0:3, 0:3]
        self.cam[0:3, 3] = self.cam[0:3, 3] + T[0:3, 3]
        self.cam_obj = np.linalg.inv(self.cam) @ self.objeto
        self.update_canvas()

    def update_cam(self,line_edits):
        values = self.read_transform_values(line_edits)

        T = move(values[0], values[2], values[4])
        Rx = x_rotation(values[1])
        Ry = y_rotation(values[3])
        Rz = z_rotation(values[5])
        R = Rz @ Ry @ Rx

        self.cam[0:3, 3] = self.cam[0:3, 3] + self.cam[0:3, 0:3] @ T[0:3, 3]
        self.cam[0:3, 0:3] = self.cam[0:3, 0:3] @ R[0:3, 0:3]
        self.cam_obj = np.linalg.inv(self.cam) @ self.objeto
        self.update_canvas()
    
    def projection_2d(self):
        self.projection_matrix = self.generate_intrinsic_params_matrix()
        proj_points = image_project(self.projection_matrix,self.cam,self.objeto)
        return proj_points
    
    def generate_intrinsic_params_matrix(self):
        sx = self.px_base / self.ccd[0]
        sy = self.px_altura / self.ccd[1]

        return array([
            [self.dist_foc * sx, self.dist_foc * self.stheta, self.ox],
            [0, self.dist_foc * sy, self.oy],
            [0, 0, 1],
        ])

    def update_canvas(self):
        self.cam_obj = np.linalg.inv(self.cam) @ self.objeto
        object_2d = self.projection_2d()

        self.ax1.clear()
        self.ax1.set_title("Imagem")
        self.ax1.set_xlim([0, self.px_base])
        self.ax1.set_ylim([self.px_altura, 0])
        self.ax1.plot(object_2d[0, :], object_2d[1, :])
        self.ax1.grid(True)
        self.ax1.set_aspect('equal')

        self.ax2.clear()
        set_plot(self.ax2, self.fig2, lim=[-5, 5])
        self.ax2 = draw_arrows(self.world[:, -1], self.world[:, 0:3], self.ax2, 3)
        self.ax2 = draw_arrows(self.cam[:, -1], self.cam[:, 0:3], self.ax2, 1)
        self.ax2.plot(self.objeto[0, :], self.objeto[1, :], self.objeto[2, :], 'r')

        self.canvas1.draw()
        self.canvas2.draw()
    
    def reset_canvas(self):
        self.set_variables()
        self.update_canvas()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
