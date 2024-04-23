import copy
import gif
import heapq
from Map.map import get_path
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap as LSC


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.preNode = None  # 记录前一个节点
        self.distance = 0  # 已经过距离，初始为零
        self.heuristic = 0  # 启发函数值

    def __lt__(self, other):
        # 重写堆的排序规则，按照优先级排序，值越小优先级越高
        return self.prioritize() < other.prioritize()

    def prioritize(self):
        # 经过距离和启发函数之和越小，优先级越高
        return self.distance + self.heuristic


# 曼哈顿距离估计
def manhattan_dist(current: Node, target: Node):
    return abs(current.x - target.x) + abs(current.y - target.y)


@gif.frame
def draw_map(map2d):
    plt.clf()
    plt.axis("off")
    colors_map = ['lightgrey', 'lightgreen', 'green', 'lightyellow', 'brown']
    cmp = LSC.from_list("color", colors_map)
    plt.imshow(map2d, cmap=cmp)


def a_star(map2d, start, goal, save=True, path="./a_star.gif", func=manhattan_dist):
    _map = copy.deepcopy(map2d)  # 对地图进行深拷贝，避免绘图对地图中数值的影响
    assert (_map[start.x][start.y] == 0 and _map[goal.x][goal.y] == 0)
    # 获取起点和终点，创建 openset 和 closeset
    open_set = []  # 存放节点，小根堆
    close_set = []  # 存放位置坐标，不在寻找已走过的位置
    heapq.heappush(open_set, start)
    # 绘制地图
    frames = [draw_map(_map)]
    while len(open_set) > 0:
        # openset 中弹出一个优先级最高的节点进行检验
        curr_node = heapq.heappop(open_set)
        if (curr_node.x, curr_node.y) == (goal.x, goal.y):
            result = []
            # 对最终结果进行溯源，找出起点到终点的路径
            while curr_node is not None:
                result.append(curr_node)
                # 绘图--openset
                _map[curr_node.x][curr_node.y] = 0.5
                frames.append(draw_map(_map))
                curr_node = curr_node.preNode
            result.reverse()
            # 保存过程图
            if save:
                gif.save(frames, path, duration=1)
            return True, result
        else:
            close_set.append((curr_node.x, curr_node.y))  # 排除当前节点
            # 绘图--closeset
            _map[curr_node.x][curr_node.y] = 0.8
            frames.append(draw_map(_map))
            # 搜寻下一个可能的节点，并加入 openset
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_node = Node(curr_node.x + dx, curr_node.y + dy)
                if (0 <= new_node.x < len(_map[0]) and 0 <= new_node.y < len(_map)
                        and _map[new_node.x][new_node.y] != 1) and (new_node.x, new_node.y) not in close_set:
                    new_node.distance = curr_node.distance + 1
                    new_node.heuristic = func(new_node, goal)  # 调用启发函数，默认为曼哈顿距离
                    new_node.preNode = curr_node
                    heapq.heappush(open_set, new_node)
                    # 绘图--path
                    _map[new_node.x][new_node.y] = 0.3
                    frames.append(draw_map(_map))
                    # 绘图过程
    return False, None


def main():
    map2d = get_path("")
    flag, path = a_star(map2d, Node(0, 0), Node(8, 18))
    if flag:
        print("成功找到路径！")
        print([(node.x, node.y) for node in path])
    else:
        print("查找路径失败！")


if __name__ == '__main__':
    main()