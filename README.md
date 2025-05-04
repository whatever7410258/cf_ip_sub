更新：  
跟大善人斗智斗勇太烦了，不搞了，分享从某论坛转换之后的订阅链接，应该是长期有效吧：  
https://sub.7410258.xyz/sub?source=linux.do.oracle&type=clash   
https://sub.7410258.xyz/sub?source=linux.do.oracle&type=v2rayn   
https://sub.7410258.xyz/sub?source=linux.do.selfuse&type=clash   

原仓库:   
https://github.com/1304756868/cf_ip_sub    
感谢原仓库大佬的贡献，我在大佬原本的HK/JP/KR基础上加了SG，节点数量直接x10，非常好用！  
另外clash规则大佬直接引用的git文本链接，在国内可能会加载失败，我改成了代理地址，国内使用无障碍。  
   
以下是仓库原始README：   
   
# cf_ip_sub
An automated program that is designed to perform daily testing and filtering of CF better IP addresses, updating into the subscribed links. Manual testing and filtering of CF better IP are no longer necessary. Simply update the subscription in Clash or V2RayN when needed.   
IP source: https://github.com/hello-earth/cloudflare-better-ip  
This program does not include the code for setting up vless nodes. If needed, please refer to: https://github.com/yonggekkk/Cloudflare-workers-pages-vless

**vlwoker.yaml**   
Better IPs will be updating into this file daily. When the CF worker is invoked, it will read the content from here.   
Rule source: https://github.com/Loyalsoldier/clash-rules

**nas**   
Program running in your nas or linux PC, performing daily testing and filtering of CF better IP addresses, updating them into "vlwoker.yaml" in this git.
You need to modify the path in "nas/cf-ip.sh" and set it to run automatically every day.

**cf-worker**   
The code filled in the CF worker.   
After deployment, subscribe through the following two links:
- clash:  
  https://<your_cf_worker_domain>/sub?servername=<your_vless_worker_domain>&type=clash&uuid=<your_uuid>
- v2rayn:  
  https://<your_cf_worker_domain>/sub?servername=<your_vless_worker_domain>&type=urls&uuid=<your_uuid>

