#pragma once

class Room
{
public:
	Room(int rid);
	~Room();

	int getRoomId();
	bool isEmpty();
	int run();
	int close();

	int addCookie(Json::Value cookie, bool status, int freq);
	int delCookie(int uid);
	int setSpeak(bool status);
	int setFreq(int freq);
	int sendBarrage(int uid, string barrage);
	void setSocketServer(SOCKET socketServer);

private:
	int m_rid;
	list<Robot*> m_robots;
	SOCKET m_socketServer;

	Robot *getRobot(int uid);
};