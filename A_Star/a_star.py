from Map.map import get_path
import matplotlib.pyplot as plt
import heapq

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.preNode = None
        self._g_ = 0
        self._h_ = 0

    def _f_(self):
        return self._g_ + self._h_

    def __lt__(self, other):
        return self._f_() < other._f_()

def a_star(map, start, goal):
    start_x, start_y = start
    goal_x, goal_y = goal
    open_set = []
    close_set = set()
    # 初始化第一个节点
    origin = Node(start_x, start_y)
    heapq.heappush(open_set, origin)
    while len(open_set) > 0:
        currNode = heapq.heappop(open_set)
        if (currNode.x, currNode.y) == (goal_x, goal_y):
            return True, currNode
        else:
            close_set.add(currNode)
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = currNode.x + dx, currNode.y + dy
                if 0 <= new_x < len(map[0]) and 0 <= new_y < len(map) and map[new_x][new_y] == 0:
                    newNode = Node(new_x, new_y)
                    newNode._g_ = currNode._g_ + 1
                    # 曼哈顿距离估计
                    newNode._h_ = abs(new_x - goal_x) + abs(new_y - goal_y)
                    newNode.preNode = currNode
                    heapq.heappush(open_set, newNode)
    return False, None

if __name__ == '__main__':
    map = get_path("")
    plt.imshow(map)
    plt.ion()
    plt.axis('off')
    start = (0,0)
    goal = (len(map)-1, len(map[0])-1)
    flag, node = a_star(map, start, goal)
    if flag:
        while node.preNode is not None:
            print(node.preNode.x, node.preNode.y)
            node = node.preNode
            map[node.x][node.y] = 0.5
            plt.clf()
            plt.cla()
            plt.axis('off')
            plt.imshow(map)
            plt.pause(0.5)
    plt.ioff()