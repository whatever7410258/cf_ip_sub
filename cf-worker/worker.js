/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

// Export a default object containing event handlers
const yaml_url = "https://raw.githubusercontent.com/whatever7410258/cf_ip_sub/main/vlworker.yaml";

export default {
  // The fetch handler is invoked when this worker receives a HTTP(S) request 
  // and should return a Response (optionally wrapped in a Promise)
  async fetch(request, env, ctx) {
    // You'll find it helpful to parse the request.url string into a URL object. Learn more at https://developer.mozilla.org/en-US/docs/Web/API/URL
    const url = new URL(request.url);


    if (url.pathname != '/sub') {
      return new Response('Not Found.', { status: 400 });
    } 

    const servername = url.searchParams.get('servername');
    const sub_type = url.searchParams.get('type'); // get a query param value (?proxyUrl=...)
    let param_uuid = url.searchParams.get('uuid');
	
    if ((!servername)||(!sub_type)) {
      return new Response('Param Error.', { status: 403 });
    } 

    let res = await fetch(yaml_url);
    let data = await res.text();
    if(sub_type == 'yaml'){
      if(param_uuid)data = data.replaceAll("your_uuid", param_uuid);
      data = data.replaceAll("host.japan.com", servername);
    }else if(sub_type == 'base64'){
      let proxies = data.split("proxies:\n-")[1].split("\nproxy-groups:")[0].split("\n-");
      let sub_urls = "";
      proxies.forEach(proxy =>{
        let lines = (" " + proxy).split("\n");
        let server = "";
        let name = "";
        lines.forEach(line => {
          if(line.startsWith("  server:")){
            server = line.split(": ")[1];
          }else if(line.startsWith("  name:")){
            name = line.split(": ")[1];
          }
        });
        let url = `vless://${param_uuid}@${server}:443?encryption=none&security=tls&sni=${servername}&type=ws&host=${servername}&path=%2F%3Fed%3D2048#${name}\n`;
        sub_urls += url;
      });
      data = btoa(sub_urls);
    }else{
      return new Response('Param Error.', { status: 403 });
    }

    return new Response(
      data,
      { headers: { "Content-Type": "text/plain" } }
    );
  },
};
