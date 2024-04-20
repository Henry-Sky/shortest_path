from Map.map import get_path
import matplotlib.pyplot as plt
import heapq


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.preNode = None  # 记录前一个节点
        self.distance = 0  # 已经过距离，初始为零
        self.heuristic = 0  # 启发函数值

    def prioritize(self):
        # 经过距离和启发函数之和越小，优先级越高
        return self.distance + self.heuristic

    def __lt__(self, other):
        # 重写堆的排序规则，按照优先级排序，值越小优先级越高
        return self.prioritize() < other.prioritize()


# 曼哈顿距离估计
def manhattan_dist(current, target):
    return abs(current.x - target.x) + abs(current.y - target.y)


def a_star(map, start, goal, func=manhattan_dist):
    assert (map[start[0]][start[1]] == 0 and map[goal[0]][goal[1]] == 0)
    # 获取起点和终点，创建 openset 和 closeset
    start_x, start_y = start
    goal_x, goal_y = goal
    open_set = []
    close_set = set()
    # 初始化第一个节点
    origin = Node(start_x, start_y)
    target = Node(goal_x, goal_y)
    heapq.heappush(open_set, origin)
    while len(open_set) > 0:
        # openset 中弹出一个优先级最高的节点进行检验
        curr_node = heapq.heappop(open_set)
        if (curr_node.x, curr_node.y) == (goal_x, goal_y):
            result = []
            # 对最终结果进行溯源，找出起点到终点的路径
            while curr_node is not None:
                result.append(curr_node)
                curr_node = curr_node.preNode
            result.reverse()
            return True, result
        else:
            close_set.add(curr_node)  # 排除当前节点
            # 搜寻下一个可能的节点，并加入 openset
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = curr_node.x + dx, curr_node.y + dy
                if (0 <= new_x < len(map[0]) and 0 <= new_y < len(map)
                        and map[new_x][new_y] != 1):
                    new_node = Node(new_x, new_y)
                    new_node.distance = curr_node.distance + 1
                    new_node.heuristic = func(new_node, target)  # 调用启发函数，默认为曼哈顿距离
                    new_node.preNode = curr_node
                    heapq.heappush(open_set, new_node)
    return False, None


def main():
    map = get_path("")
    flag, path = a_star(map, (0, 0), (18, 18))
    if flag:
        # 开始绘图
        plt.ion()
        for node in path:
            plt.clf()
            plt.axis("off")
            map[node.x][node.y] = 0.5
            plt.imshow(map)
            plt.pause(0.5)
        plt.ioff()


if __name__ == '__main__':
    main()
