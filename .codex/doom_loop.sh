#!/bin/bash
# 反循环闸门（默认 dry-run）：同一 shell 命令在 25 秒窗口内连续重复 3 次时记录事件，不拦截。
# 状态按会话隔离；目录默认 ~/.codex/doom_loop，可用 CODEX_DOOM_LOOP_DIR 覆盖；时间可用 CODEX_DOOM_LOOP_NOW 注入（测试用）。
# 安全设计：只有显式 intercept 模式才以退出码 2 拦截；脚本自身出错一律放行，不阻塞正常工具调用。
input=$(cat)
tmp=$(mktemp)
printf '%s' "$input" > "$tmp"
node -e 'const fs=require("fs");const path=require("path");const os=require("os");
const o=JSON.parse(fs.readFileSync(process.argv[1],"utf8"));
const ti=o.tool_input;let cmd="";
try{const obj=typeof ti==="object"?ti:JSON.parse(ti);cmd=obj.cmd||obj.command||obj.input||""}catch(e){cmd=typeof ti==="object"?(ti.cmd||ti.command||ti.input||""):String(ti||"")}
cmd=String(cmd).trim();if(!cmd)process.exit(0);
const session=String(o.session_id||"unknown").replace(/[^A-Za-z0-9_-]/g,"_")||"unknown";
const dir=process.env.CODEX_DOOM_LOOP_DIR||path.join(os.homedir(),".codex","doom_loop");
fs.mkdirSync(dir,{recursive:true});
const stateFile=path.join(dir,"state_"+session+".json");
const logFile=path.join(dir,"events.log");
const now=process.env.CODEX_DOOM_LOOP_NOW?Number(process.env.CODEX_DOOM_LOOP_NOW):Math.floor(Date.now()/1000);
const windowSec=Number(process.env.CODEX_DOOM_LOOP_WINDOW||25);
const threshold=Number(process.env.CODEX_DOOM_LOOP_THRESHOLD||3);
let st={cmd:"",count:0,ts:0};
try{st=JSON.parse(fs.readFileSync(stateFile,"utf8"))}catch(e){}
if(st.cmd===cmd&&now-st.ts<=windowSec){st.count+=1}else{st.count=1;st.cmd=cmd}
st.ts=now;
fs.writeFileSync(stateFile,JSON.stringify(st));
if(st.count>=threshold){
  const ev=JSON.stringify({ts:new Date(now*1000).toISOString(),session,cmd,cwd:o.cwd||"",count:st.count,mode:process.env.CODEX_DOOM_LOOP_MODE==="intercept"?"intercept":"dry-run"})+"\n";
  fs.appendFileSync(logFile,ev);
  if(process.env.CODEX_DOOM_LOOP_MODE==="intercept"){process.stderr.write("拦截：疑似循环重试（同一命令连续 "+st.count+" 次），请换思路\n");process.exit(2)}
}
process.exit(0);' "$tmp"
rc=$?
rm -f "$tmp"
if [ "$rc" -eq 2 ]; then exit 2; fi
exit 0
