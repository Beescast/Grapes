#pragma once

#define MAX_ROOM_NUM	100

class Manage
{
public:
	Manage();
	~Manage();

	int addCookie(int rid, Json::Value cookie, bool status, int freq);
	int delCookie(int rid, int uid);
	int setSpeak(int rid, bool status);
	int setFreq(int rid, int freq);
	int sendBarrage(int rid, int uid, string barrage);
	int delRoom(int rid);
	void setSocketServer(SOCKET socketServer);
	SOCKET getSocketServer();
	int close();

private:
	int addRoom(int rid);
	bool inRooms(int rid);
	Room *getRoom(int rid);
	list<Room*> m_rooms;
	SOCKET m_socketServer;
};