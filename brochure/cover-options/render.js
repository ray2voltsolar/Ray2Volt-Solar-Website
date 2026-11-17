// Renders cover options into the real cover layout and screenshots them.
// Usage: node render.js <options.json> <output-prefix>
const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const root=path.join(__dirname,'..');const b64=f=>fs.readFileSync(f).toString('base64');
const opts=JSON.parse(fs.readFileSync(path.join(__dirname,process.argv[2])));const pre=process.argv[3]||'';
let fonts=fs.readFileSync(path.join(root,'fonts/fonts.css'),'utf8').replace(/url\(([^)]+\.woff2)\)/g,(m,f)=>`url(data:font/woff2;base64,${b64(path.join(root,'fonts',f))})`);
const css=fs.readFileSync(path.join(root,'src/base.css'),'utf8');
const logo=`data:image/png;base64,${b64(path.join(root,'..','images','logo.png'))}`;
const tpl=fs.readFileSync(path.join(root,'src/pages/01-cover.html'),'utf8').replace(/\{\{LOGO\}\}/g,logo);
(async()=>{const br=await chromium.launch();const pg=await br.newPage({viewport:{width:794,height:1123},deviceScaleFactor:2});
for(const [name,v] of Object.entries(opts)){
  const o=typeof v==='string'?{svg:v}:v;
  const html=tpl.replace(/<div class="photo">[\s\S]*?<\/svg>(<div class="bar"><\/div>)?<\/div>/,`<div class="photo">${o.svg}</div>`);
  await pg.setContent(`<!doctype html><meta charset="utf-8"><style>${fonts}${css} body{background:#fff}.page{margin:0!important;box-shadow:none!important}</style>${html}<style>.p01 .photo{background:none!important}${o.css||''}</style>`);
  await pg.evaluate(()=>document.fonts.ready);
  await (await pg.$('.page')).screenshot({path:path.join(__dirname,pre+name.trim().split(/\s+/)[0]+'.png')});
}
await br.close();})();
