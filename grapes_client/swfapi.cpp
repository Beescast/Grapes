
#include "stdafx.h"
#include "swfapi.h"

#pragma comment(lib, "ws2_32.lib")

Swfapi::Swfapi()
{
}

Swfapi::~Swfapi()
{
}

Json::Value Swfapi::xxSwfApi(Json::Value req)
{
	req["req_t"] = to_string(time(nullptr));
	char buff[MAX_RECV_SIZE] = { 0 };
	SOCKADDR_IN addrSrv;
	addrSrv.sin_family = AF_INET;
	addrSrv.sin_port = htons(SWFAPI_PORT);
	addrSrv.sin_addr.s_addr = inet_addr(SWFAPI_IP);
	SOCKET sockClient = socket(AF_INET, SOCK_STREAM, 0);
	if (SOCKET_ERROR == sockClient) {
#ifdef _DEBUG
		cout << "Socket() error:" << WSAGetLastError() << endl;
#endif // _DEBUG
		return -1;
	}
	int result = connect(sockClient, (struct  sockaddr*)&addrSrv, sizeof(addrSrv));
	if (INVALID_SOCKET == result)
	{
#ifdef _DEBUG
		cout << "Connect failed:" << WSAGetLastError() << endl;
#endif // _DEBUG
		return -1;
	}
	string req_str = req.toStyledString();
	if (send(sockClient, req_str.c_str(), req_str.length(), 0) <= 0)
	{
#ifdef _DEBUG
		cout << "Send failed:" << WSAGetLastError() << endl;
#endif // _DEBUG
		return -1;
	}
	if (recv(sockClient, buff, MAX_RECV_SIZE, 0) > 0)
	{
#ifdef _DEBUG
		cout << "xxSwfApi: " << buff << endl;
#endif // _DEBUG
		Json::Reader reader = Json::Reader();
		Json::Value rsp = Json::Value();
		reader.parse(buff, rsp);
		Json::Value rst = deserialize(rsp["result"].asString());
		Json::Value data = Json::Value();
		data["dict"] = rst;
		data["text"] = rsp["result"];
		return data;
	}
	return Json::Value();
}
