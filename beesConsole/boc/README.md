# Install

    $ mysql -uroot -p bocms < bocadmin/setup/db.sql
    $ sudo cp bocadmin/setup/nginx.vhost.conf /etc/nginx/vhost/bocms.conf
    $ sudo vim /etc/nginx/vhost/bocms.conf
    $ chmod 777 adminer/cache/ adminer/logs/ site/cache/ site/logs/ upload/


修改 config.php



UPDATE:

15.5.14

* bselect
    修改 columns_model 添加 get_tree
    修改 coltypes_model 添加 get_tree
    修改 uiadmin_helper 添加 ui_tree 修改了 ui_btn_select
    修改对应 data_helper 的 list_coltypes 引用位置
    修改 columns, coltypes 模板对应引用位置

15.4.2 AMD 和 媒体上传

* AMD规范

    使用 require.js  和 require.conf.js 来异步处理所有的js事件，加速页面呈现

* media 修改

    添加了media.init(upload_done, del_done)，其中 upload_done 为上传结束后执行的callback，del_done为删除操作后的callback
    基本使用为

    media.init();
    media.show(tdata,input_name)

    注意修改
    对 上传字段添加 form 验证规则 ，trim ，这样错误的时候上传数据不会丢失

    为 file 上传控件添加 data-width data-height 可以压缩上传图片。

    编辑器上传图片压缩默认值在 配置中心中设置。
