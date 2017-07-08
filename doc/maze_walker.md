MazeWaler思路：
未探索：蓝色
已经过：黄色
已标记：红色

Agent: 绿色小方块

unexplored_list = [];
passed_list = [];
marked_list = [];

RoomList = {};
GateList = {};

Room:格子对象

Gate:记录Room间的连接关系

Agent:行为：从当前格子的中心移动到目标格子中心，移动到中心时，执行判断逻辑，决定往哪个方向走。

Brain:移动方向决策

Main:
State:1 => 编辑模式
State:2 => 训练模式
State:3 => 测试模式

窗口大小：640 * 640
每个格子大小：32*32
方向键：按照格子移动游标
SPACE键：放置或消除格子

1,如果passed_list和marked_list为空，则从unexplored_list中随机选一个位置，将选好的对象从unexplored_list中取出来放入passed_list中，如果passed_list不为空则从中随机一个位置，如果passed_list为空，marked_list不为空，则从marked_list随机一个位置
2,每次迭代时要做的事情
	1，查询当前格子的邻居，如果只有未探索的邻居和已经过的邻居，则从未探索的邻居中随机一个走过去，并把当前格子标记为已经过（将颜色变为黄色）；如果存在已标记的邻居和未探索的邻居，则随机一下决定是走标记过的邻居还是未探索的邻居，不考虑已经过的邻居，如果选择了未探索的邻居则当前各自标记为已经过（将颜色设置为黄色），如果选择了已标记过的邻居则当前格子标记为已经过（颜色这是为红色）。如果当前格子没有已标记的邻居也没有未探索的邻居，则以门的计数器作为权重随机决定前往那个邻居，前往已标记过的邻居时，更新权重。
	2,如果unexplored_list和passed_list都为空，则停机。

