# 基础数学库实现 
class Vec2:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vec2(self.x * scalar, self.y * scalar)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y

class Vec3:
    __slots__ = ('x', 'y', 'z')
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def normalize(self):
        mag = (self.x**2 + self.y**2 + self.z**2) ** 0.5
        return Vec3(self.x/mag, self.y/mag, self.z/mag) if mag > 0 else self

class Mat4:
    def __init__(self, data=None):
        self.data = data or [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]
    
    def perspective(fov, aspect, near, far):
        f = 1.0 / (fov ** 0.5)
        range_inv = 1.0 / (near - far)
        return Mat4([
            [f/aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (near+far)*range_inv, -1],
            [0, 0, near*far*range_inv*2, 0]
        ])
    
    def look_at(eye, target, up):
        z = (eye - target).normalize()
        x = up.cross(z).normalize()
        y = z.cross(x)
        return Mat4([
            [x.x, x.y, x.z, -x.dot(eye)],
            [y.x, y.y, y.z, -y.dot(eye)],
            [z.x, z.y, z.z, -z.dot(eye)],
            [0, 0, 0, 1]
        ])
    
    def __mul__(self, other):
        if isinstance(other, Vec3):
            v = [other.x, other.y, other.z, 1]
            out = [0,0,0,0]
            for i in range(4):
                for j in range(4):
                    out[i] += self.data[i][j] * v[j]
            w = out[3]
            return Vec3(out[0]/w, out[1]/w, out[2]/w) if w != 0 else Vec3(0,0,0)
        return self

# 3D模型处理 
class Mesh:
    def __init__(self):
        self.vertices = []
        self.faces = []
    
    def create_cube():
        mesh = Mesh()
        mesh.vertices = [
            Vec3(-1,-1,-1), Vec3(1,-1,-1), Vec3(1,1,-1), Vec3(-1,1,-1),
            Vec3(-1,-1,1), Vec3(1,-1,1), Vec3(1,1,1), Vec3(-1,1,1)
        ]
        mesh.faces = [
            (0,1,2), (0,2,3), (4,5,6), (4,6,7),
            (0,4,7), (0,7,3), (1,5,6), (1,6,2),
            (0,1,5), (0,5,4), (3,2,6), (3,6,7)
        ]
        return mesh

# 软件渲染器核心
class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.framebuffer = [0] * (width * height)
        self.depth_buffer = [1e30] * (width * height)  # 使用大数代替无穷大
        self.clear_color = 0
        self.light_dir = Vec3(0, 0, -1).normalize()
    
    def clear(self):
        for i in range(self.width * self.height):
            self.framebuffer[i] = self.clear_color
            self.depth_buffer[i] = 1e30
    
    def set_pixel(self, x, y, color, depth):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        idx = y * self.width + x
        if depth < self.depth_buffer[idx]:
            self.framebuffer[idx] = color
            self.depth_buffer[idx] = depth
    
    def draw_triangle(self, v0, v1, v2, color):
        # 包围盒计算
        min_x = min(v0.x, v1.x, v2.x)
        max_x = max(v0.x, v1.x, v2.x)
        min_y = min(v0.y, v1.y, v2.y)
        max_y = max(v0.y, v1.y, v2.y)
        
        # 光栅化循环
        for y in range(int(min_y), int(max_y) + 1):
            for x in range(int(min_x), int(max_x) + 1):
                p = Vec2(x, y)
                # 计算重心坐标
                denom = ((v1.y - v2.y)*(v0.x - v2.x) + (v2.x - v1.x)*(v0.y - v2.y))
                if abs(denom) < 1e-6:  # 避免除零
                    continue
                
                w0 = ((v1.y - v2.y)*(p.x - v2.x) + (v2.x - v1.x)*(p.y - v2.y)) / denom
                w1 = ((v2.y - v0.y)*(p.x - v2.x) + (v0.x - v2.x)*(p.y - v2.y)) / denom
                w2 = 1 - w0 - w1
                
                if w0 >= 0 and w1 >= 0 and w2 >= 0:
                    # 深度插值
                    depth = w0*v0.z + w1*v1.z + w2*v2.z
                    self.set_pixel(x, y, color, depth)
    
    def render_mesh(self, mesh, view_matrix, proj_matrix):
        view_proj = proj_matrix * view_matrix
        for face in mesh.faces:
            # 顶点变换
            v0 = view_proj * mesh.vertices[face[0]]
            v1 = view_proj * mesh.vertices[face[1]]
            v2 = view_proj * mesh.vertices[face[2]]
            
            # 背面剔除
            edge1 = v1 - v0
            edge2 = v2 - v0
            normal = edge1.cross(edge2)
            if normal.z > 0:  # 只渲染面向摄像机的面
                continue
            
            # 屏幕空间变换
            v0 = Vec3((v0.x + 1) * 0.5 * self.width, (1 - v0.y) * 0.5 * self.height, v0.z)
            v1 = Vec3((v1.x + 1) * 0.5 * self.width, (1 - v1.y) * 0.5 * self.height, v1.z)
            v2 = Vec3((v2.x + 1) * 0.5 * self.width, (1 - v2.y) * 0.5 * self.height, v2.z)
            
            # 光照计算
            intensity = max(0.2, -normal.normalize().dot(self.light_dir))
            color = int(intensity * 255) * 0x10101
            
            self.draw_triangle(v0, v1, v2, color)
    
    def render_to_ascii(self):
        """将渲染结果转换为ASCII艺术"""
        ascii_chars = " .:-=+*#%@"
        output = []
        for y in range(self.height):
            line = []
            for x in range(self.width):
                color = self.framebuffer[y * self.width + x]
                # 提取亮度分量
                brightness = (color >> 16) & 0xFF
                # 映射到ASCII字符
                char_idx = int(brightness / 255 * (len(ascii_chars) - 1))
                line.append(ascii_chars[char_idx])
            output.append(''.join(line))
        return '\n'.join(output)

# 主程序
def main():
    WIDTH, HEIGHT = 80, 40  # 使用较小的分辨率适合ASCII输出
    
    # 创建渲染器
    renderer = Renderer(WIDTH, HEIGHT)
    renderer.clear()
    
    # 创建立方体模型
    mesh = Mesh.create_cube()
    
    # 设置摄像机
    eye = Vec3(3, 2, 4)
    target = Vec3(0, 0, 0)
    up = Vec3(0, 1, 0)
    
    # 创建变换矩阵
    view = Mat4.look_at(eye, target, up)
    proj = Mat4.perspective(0.8, WIDTH/HEIGHT, 0.1, 100)
    
    # 渲染场景
    renderer.render_mesh(mesh, view, proj)
    
    # 输出ASCII艺术
    print(renderer.render_to_ascii())

# 手动调用主函数
if __name__ == '__main__':
    main()