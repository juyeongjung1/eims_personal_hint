import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT = path.join(ROOT, "Java個人演習_タイピングテストアプリ_講師向けマニュアル.pptx");
const PREVIEW_DIR = path.join(ROOT, "outputs", "instructor-manual-preview");
const runtimeRoot = path.join(
  process.env.USERPROFILE || process.env.HOME,
  ".cache",
  "codex-runtimes",
  "codex-primary-runtime",
  "dependencies",
  "node",
  "node_modules",
  "@oai",
  "artifact-tool",
  "dist",
  "artifact_tool.mjs",
);

const artifact = await import(pathToFileURL(runtimeRoot).href);
const { Presentation, PresentationFile } = artifact;

const W = 1280;
const H = 720;
const C = {
  bg: "#F7F8F5",
  paper: "#FFFFFF",
  ink: "#1D2528",
  muted: "#5B676C",
  line: "#D9DFDC",
  green: "#1F7A62",
  greenSoft: "#E6F3EE",
  amber: "#946200",
  amberSoft: "#FFF3D6",
  blue: "#2F5F9E",
  blueSoft: "#EAF3FF",
  cyan: "#C7F0FF",
  red: "#B43D2D",
  dark: "#22312E",
};

function addShape(slide, { x, y, w, h, fill = "#00000000", line = "#00000000", lineWidth = 0, geometry = "rect", name }) {
  return slide.shapes.add({
    geometry,
    name,
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: { style: "solid", fill: line, width: lineWidth },
  });
}

function addText(
  slide,
  text,
  { x, y, w, h, size = 24, color = C.ink, bold = false, align = "left", valign = "top", fill = "#00000000", line = "#00000000", inset = 0, name } = {},
) {
  const shape = addShape(slide, { x, y, w, h, fill, line, lineWidth: line === "#00000000" ? 0 : 1, name });
  shape.text = text;
  shape.text.fontSize = size;
  shape.text.typeface = "Meiryo";
  shape.text.color = color;
  shape.text.bold = bold;
  shape.text.alignment = align;
  shape.text.verticalAlignment = valign;
  shape.text.insets = { left: inset, right: inset, top: inset, bottom: inset };
  return shape;
}

function addLine(slide, x1, y1, x2, y2, color = C.line, width = 2) {
  const x = Math.min(x1, x2);
  const y = Math.min(y1, y2);
  const w = Math.max(Math.abs(x2 - x1), width);
  const h = Math.max(Math.abs(y2 - y1), width);
  return addShape(slide, { x, y, w, h, fill: color, line: color });
}

function addHeader(slide, kicker, title, page) {
  addShape(slide, { x: 0, y: 0, w: W, h: H, fill: C.bg });
  addText(slide, kicker, { x: 56, y: 34, w: 260, h: 24, size: 14, color: C.green, bold: true });
  addText(slide, title, { x: 56, y: 60, w: 930, h: 58, size: 31, color: C.ink, bold: true });
  addText(slide, String(page).padStart(2, "0"), { x: 1174, y: 46, w: 52, h: 30, size: 15, color: C.muted, align: "right" });
  addLine(slide, 56, 126, 1224, 126, C.line, 2);
}

function chip(slide, text, x, y, w, fill = C.greenSoft, color = C.green) {
  addText(slide, text, { x, y, w, h: 30, size: 15, color, bold: true, align: "center", valign: "middle", fill, line: "#B9D8CB", inset: 4 });
}

function bullet(slide, text, x, y, w, accent = C.green) {
  addShape(slide, { x, y: y + 9, w: 8, h: 8, fill: accent, line: accent });
  addText(slide, text, { x: x + 18, y, w, h: 42, size: 18, color: C.ink });
}

function screenFrame(slide, x, y, w, h, title = "Java個人演習「タイピングテストアプリ」") {
  addShape(slide, { x, y, w, h, fill: "#FFFFFF", line: "#C9D3CF", lineWidth: 1 });
  addShape(slide, { x, y, w, h: 38, fill: "#EEF4F1", line: "#C9D3CF", lineWidth: 1 });
  addShape(slide, { x: x + 15, y: y + 14, w: 9, h: 9, fill: "#FF6B6B", line: "#FF6B6B" });
  addShape(slide, { x: x + 31, y: y + 14, w: 9, h: 9, fill: "#FFD166", line: "#FFD166" });
  addShape(slide, { x: x + 47, y: y + 14, w: 9, h: 9, fill: "#4ECDC4", line: "#4ECDC4" });
  addText(slide, title, { x: x + 74, y: y + 8, w: w - 100, h: 22, size: 12, color: C.muted });
}

function drawTopbarMock(slide, x, y, w) {
  addShape(slide, { x, y, w, h: 88, fill: "#F7F8F5", line: C.line, lineWidth: 1 });
  addText(slide, "Java個人演習", { x: x + 18, y: y + 16, w: 150, h: 24, size: 12, color: C.green, bold: true });
  addShape(slide, { x: x + 180, y: y + 12, w: 270, h: 34, fill: "#FFFFFF", line: C.line, lineWidth: 1 });
  addText(slide, "演習番号・用語・コードを検索", { x: x + 192, y: y + 20, w: 240, h: 20, size: 11, color: C.muted });
  addText(slide, "15件表示中", { x: x + 465, y: y + 20, w: 78, h: 20, size: 11, color: C.muted, align: "right" });
  addText(slide, "講師用", { x: x + w - 86, y: y + 12, w: 68, h: 34, size: 11, color: C.ink, bold: true, align: "center", valign: "middle", fill: "#FFFFFF", line: C.line, inset: 3 });
  ["すべて", "演習1", "演習2", "演習3", "演習4", "演習5"].forEach((label, i) => {
    addText(slide, label, { x: x + 18 + i * 64, y: y + 54, w: 54, h: 24, size: 10, color: i === 0 ? "#FFFFFF" : C.ink, bold: true, align: "center", valign: "middle", fill: i === 0 ? C.green : "#FFFFFF", line: C.line, inset: 2 });
  });
}

function drawExerciseCard(slide, x, y, w, title, status, locked = false) {
  addShape(slide, { x, y, w, h: locked ? 92 : 126, fill: locked ? "#FFFDF7" : "#FFFFFF", line: locked ? "#E3BD66" : C.line, lineWidth: 1 });
  addText(slide, title, { x: x + 18, y: y + 14, w: 250, h: 28, size: 17, bold: true, color: C.ink });
  addText(slide, status, { x: x + w - 130, y: y + 14, w: 104, h: 24, size: 11, color: locked ? C.amber : C.green, bold: true, align: "center", valign: "middle", fill: locked ? C.amberSoft : C.greenSoft, line: locked ? "#E3BD66" : "#B9D8CB", inset: 2 });
  if (locked) {
    addText(slide, "このヒントは 6/9 11:00公開です。\n公開時刻になると数秒以内に表示されます。", { x: x + 18, y: y + 50, w: w - 36, h: 34, size: 12, color: "#654700", bold: true, fill: "#FFF8E7", line: "#E3BD66", inset: 8 });
  } else {
    addText(slide, "参照テキスト・コード・重要ポイントを整理。穴埋めは黄色、検索ヒットは水色で表示。", { x: x + 18, y: y + 52, w: w - 36, h: 44, size: 12, color: C.muted });
  }
}

function slide1(p) {
  const slide = p.slides.add();
  addShape(slide, { x: 0, y: 0, w: W, h: H, fill: C.dark });
  addShape(slide, { x: 0, y: 0, w: 18, h: H, fill: C.green });
  addText(slide, "Java個人演習「タイピングテストアプリ」", { x: 76, y: 80, w: 520, h: 28, size: 18, color: "#9FE2C8", bold: true });
  addText(slide, "ヒント資料\n講師向けマニュアル", { x: 76, y: 132, w: 760, h: 150, size: 50, color: "#FFFFFF", bold: true });
  addText(slide, "公開時間制御・講師用モード・検索ハイライト・当日運用の確認ポイント", { x: 80, y: 316, w: 760, h: 46, size: 21, color: "#D7E3DE" });
  screenFrame(slide, 805, 130, 355, 280);
  drawTopbarMock(slide, 825, 185, 315);
  drawExerciseCard(slide, 835, 285, 295, "演習1.1 のヒント", "公開中", false);
  addText(slide, "2026/6/9・6/10 実施予定", { x: 80, y: 610, w: 360, h: 28, size: 18, color: "#FFFFFF", bold: true });
  return slide;
}

function slide2(p) {
  const slide = p.slides.add();
  addHeader(slide, "全体像", "受講者にはローカルHTMLを配布し、演習ごとの時刻でヒントを公開します", 2);
  addText(slide, "受講者側", { x: 76, y: 172, w: 180, h: 30, size: 21, bold: true, color: C.green });
  ["インターネット不要。HTMLファイルをブラウザで開く", "PCの現在日時を見て、公開前の演習は本文を隠す", "検索バー・演習タブ・コードコピーが利用可能"].forEach((t, i) => bullet(slide, t, 88, 222 + i * 60, 500));
  addText(slide, "講師側", { x: 690, y: 172, w: 180, h: 30, size: 21, bold: true, color: C.blue });
  ["右上の「講師用」からログイン", "公開前でも全ヒントを確認可能", "このPCだけ公開日時を変更して動作確認可能"].forEach((t, i) => bullet(slide, t, 702, 222 + i * 60, 500, C.blue));
  addShape(slide, { x: 76, y: 505, w: 1128, h: 88, fill: C.amberSoft, line: "#E3BD66", lineWidth: 1 });
  addText(slide, "注意", { x: 104, y: 526, w: 74, h: 30, size: 18, bold: true, color: C.amber });
  addText(slide, "ローカルHTMLの時刻制御は厳密なアクセス制御ではありません。通常運用でヒント公開タイミングを整えるための仕組みです。", { x: 190, y: 520, w: 950, h: 42, size: 18, color: C.ink });
  return slide;
}

function slide3(p) {
  const slide = p.slides.add();
  addHeader(slide, "受講者画面", "演習タブ・検索・公開状態が1画面で分かる構成です", 3);
  screenFrame(slide, 72, 164, 760, 420);
  drawTopbarMock(slide, 95, 218, 715);
  drawExerciseCard(slide, 118, 335, 312, "演習1.1 のヒント", "公開中", false);
  drawExerciseCard(slide, 465, 335, 312, "演習1.2 のヒント", "6/9 11:00公開", true);
  addText(slide, "画面の読み方", { x: 890, y: 170, w: 260, h: 32, size: 23, bold: true, color: C.green });
  bullet(slide, "タブで演習1〜5を切り替え", 902, 226, 300);
  bullet(slide, "公開前は本文を隠し、公開予定だけ表示", 902, 286, 300);
  bullet(slide, "検索すると一致箇所を水色で表示", 902, 346, 300, C.blue);
  bullet(slide, "穴埋め箇所は黄色で表示", 902, 406, 300, C.amber);
  return slide;
}

function slide4(p) {
  const slide = p.slides.add();
  addHeader(slide, "公開スケジュール", "6/9は演習1〜3、6/10は演習4〜5を段階的に公開します", 4);
  const rows = [
    ["6/9", "10:20", "演習1.1"],
    ["6/9", "11:00", "演習1.2"],
    ["6/9", "11:30", "演習2.1"],
    ["6/9", "12:00", "演習2.2"],
    ["6/9", "13:40", "演習2.3"],
    ["6/9", "14:20", "演習3.1"],
    ["6/9", "14:40", "演習3.2"],
    ["6/9", "15:40", "演習3.3"],
    ["6/10", "10:40", "演習4.1〜4.3"],
    ["6/10", "11:30", "演習5.1"],
    ["6/10", "11:50", "演習5.2"],
    ["6/10", "14:10", "演習5.3"],
    ["6/10", "15:30", "演習5.4"],
  ];
  addShape(slide, { x: 82, y: 168, w: 1114, h: 410, fill: "#FFFFFF", line: C.line, lineWidth: 1 });
  rows.forEach((r, i) => {
    const col = i < 8 ? 0 : 1;
    const row = col === 0 ? i : i - 8;
    const x = col === 0 ? 120 : 680;
    const y = 196 + row * 42;
    addText(slide, r[0], { x, y, w: 74, h: 28, size: 15, color: C.muted, bold: true });
    addText(slide, r[1], { x: x + 86, y, w: 86, h: 28, size: 16, color: C.blue, bold: true });
    addText(slide, r[2], { x: x + 184, y, w: 230, h: 28, size: 16, color: C.ink, bold: true });
    addLine(slide, x, y + 34, x + 410, y + 34, "#E7ECE9", 1);
  });
  addText(slide, "講師が変更した公開日時は、そのPCのブラウザだけに保存されます。配布HTML自体の初期スケジュールは変わりません。", { x: 120, y: 620, w: 990, h: 34, size: 17, color: C.muted });
  return slide;
}

function slide5(p) {
  const slide = p.slides.add();
  addHeader(slide, "講師用モード", "右上のボタンからログインすると、公開前でも全ヒントを確認できます", 5);
  screenFrame(slide, 72, 156, 620, 420);
  drawTopbarMock(slide, 96, 210, 570);
  addShape(slide, { x: 474, y: 216, w: 78, h: 36, fill: "#FFFFFF", line: C.blue, lineWidth: 2 });
  addText(slide, "講師用", { x: 480, y: 223, w: 66, h: 20, size: 11, bold: true, color: C.blue, align: "center" });
  addShape(slide, { x: 385, y: 276, w: 260, h: 194, fill: "#FFFFFF", line: "#BDC9C4", lineWidth: 1 });
  addText(slide, "講師用メニュー", { x: 405, y: 298, w: 150, h: 24, size: 16, bold: true });
  addShape(slide, { x: 405, y: 338, w: 155, h: 30, fill: "#FFFFFF", line: C.line, lineWidth: 1 });
  addText(slide, "パスワード", { x: 416, y: 345, w: 90, h: 18, size: 11, color: C.muted });
  addText(slide, "ログイン", { x: 568, y: 338, w: 58, h: 30, size: 11, bold: true, align: "center", valign: "middle", fill: C.greenSoft, line: "#B9D8CB", inset: 3 });
  addText(slide, "ログイン後", { x: 744, y: 184, w: 200, h: 32, size: 23, color: C.green, bold: true });
  bullet(slide, "パスワード: welcome2026", 756, 242, 380);
  bullet(slide, "「全ヒントを強制表示」で公開前も確認", 756, 302, 380);
  bullet(slide, "パネル外クリックまたはEscで閉じる", 756, 362, 380);
  addShape(slide, { x: 756, y: 470, w: 390, h: 76, fill: C.blueSoft, line: "#B7D3EE", lineWidth: 1 });
  addText(slide, "講師用ログインは、操作ミス防止のための簡易制御です。厳密なセキュリティ用途ではありません。", { x: 778, y: 490, w: 338, h: 38, size: 16, color: C.ink });
  return slide;
}

function slide6(p) {
  const slide = p.slides.add();
  addHeader(slide, "動作確認", "公開時刻をこのPCだけ変更して、受講者表示を事前確認できます", 6);
  addText(slide, "確認手順", { x: 74, y: 170, w: 180, h: 32, size: 24, bold: true, color: C.green });
  [
    "講師用にログインする",
    "「全ヒントを強制表示」をOFFにする",
    "確認したい演習の日時を現在時刻の数分前／数分後に変更",
    "「このPCに保存」を押す",
    "数秒以内に公開状態が更新されることを確認",
  ].forEach((t, i) => {
    addText(slide, `${i + 1}`, { x: 88, y: 226 + i * 62, w: 34, h: 34, size: 18, color: "#FFFFFF", bold: true, align: "center", valign: "middle", fill: C.green, inset: 2 });
    addText(slide, t, { x: 140, y: 226 + i * 62, w: 508, h: 38, size: 18, color: C.ink });
  });
  addShape(slide, { x: 700, y: 178, w: 460, h: 340, fill: "#FFFFFF", line: "#BDC9C4", lineWidth: 1 });
  addText(slide, "講師用メニュー", { x: 728, y: 204, w: 180, h: 26, size: 17, bold: true });
  addText(slide, "□ 全ヒントを強制表示", { x: 728, y: 250, w: 230, h: 26, size: 15, color: C.ink });
  addText(slide, "このPCに保存", { x: 965, y: 245, w: 110, h: 34, size: 12, bold: true, align: "center", valign: "middle", fill: C.greenSoft, line: "#B9D8CB", inset: 3 });
  addText(slide, "演習1.1", { x: 730, y: 310, w: 78, h: 24, size: 13, bold: true });
  addText(slide, "2026-06-09T10:20", { x: 824, y: 306, w: 190, h: 32, size: 13, fill: "#FFFFFF", line: C.line, inset: 5 });
  addText(slide, "演習1.2", { x: 730, y: 356, w: 78, h: 24, size: 13, bold: true });
  addText(slide, "2026-06-09T11:00", { x: 824, y: 352, w: 190, h: 32, size: 13, fill: "#FFFFFF", line: C.line, inset: 5 });
  addShape(slide, { x: 724, y: 438, w: 385, h: 48, fill: C.amberSoft, line: "#E3BD66", lineWidth: 1 });
  addText(slide, "強制表示ONのままだと、時刻に関係なく全部見えます。", { x: 744, y: 452, w: 338, h: 20, size: 15, bold: true, color: C.amber });
  return slide;
}

function slide7(p) {
  const slide = p.slides.add();
  addHeader(slide, "検索とハイライト", "検索語に一致した箇所は水色、穴埋めは黄色で区別します", 7);
  screenFrame(slide, 78, 164, 720, 372);
  drawTopbarMock(slide, 102, 218, 670);
  addShape(slide, { x: 290, y: 230, w: 84, h: 22, fill: C.cyan, line: "#1A8FB8", lineWidth: 1 });
  addText(slide, "Score", { x: 302, y: 232, w: 58, h: 18, size: 11, color: "#063547", bold: true, align: "center" });
  addShape(slide, { x: 118, y: 330, w: 632, h: 138, fill: "#FBFCFA", line: "#CCD8D3", lineWidth: 1 });
  addText(slide, 'Score score = new Score("____", ____, "test");', { x: 145, y: 360, w: 540, h: 26, size: 18, color: C.ink });
  addShape(slide, { x: 145, y: 361, w: 55, h: 24, fill: C.cyan, line: "#1A8FB8", lineWidth: 1 });
  addText(slide, "Score", { x: 149, y: 363, w: 46, h: 18, size: 14, color: "#063547", bold: true, align: "center" });
  addShape(slide, { x: 332, y: 361, w: 47, h: 24, fill: "#FFE08A", line: "#C88A00", lineWidth: 1 });
  addText(slide, "____", { x: 336, y: 363, w: 39, h: 18, size: 14, color: "#241600", bold: true, align: "center" });
  addText(slide, "使い分け", { x: 858, y: 178, w: 170, h: 32, size: 23, bold: true, color: C.green });
  addShape(slide, { x: 870, y: 240, w: 32, h: 22, fill: C.cyan, line: "#1A8FB8", lineWidth: 1 });
  addText(slide, "検索キーワードに一致した箇所", { x: 916, y: 236, w: 270, h: 30, size: 18 });
  addShape(slide, { x: 870, y: 305, w: 32, h: 22, fill: "#FFE08A", line: "#C88A00", lineWidth: 1 });
  addText(slide, "受講者が埋める穴埋め箇所", { x: 916, y: 301, w: 270, h: 30, size: 18 });
  addText(slide, "公開前の演習は、本文を検索対象にしません。受講者が公開前ヒントを検索で見つけることを避けるためです。", { x: 870, y: 392, w: 300, h: 76, size: 16, color: C.muted });
  return slide;
}

function slide8(p) {
  const slide = p.slides.add();
  addHeader(slide, "当日チェックリスト", "配布前・演習中・終了後に見るポイントです", 8);
  const columns = [
    ["配布前", ["HTMLをChrome/Edgeで開けるか確認", "講師用ログインができるか確認", "初期公開時刻が日程表どおりか確認"]],
    ["演習中", ["強制表示OFFで公開状態を確認", "公開時刻後、数秒以内に表示されるか確認", "検索語が水色で見えるか確認"]],
    ["終了後", ["必要ならPPT/HTMLをGitHubから再取得", "講師用で変更したローカル時刻は初期化", "次回日程が変わる場合はスケジュールを更新"]],
  ];
  columns.forEach((col, i) => {
    const x = 72 + i * 390;
    addShape(slide, { x, y: 172, w: 340, h: 340, fill: "#FFFFFF", line: C.line, lineWidth: 1 });
    addText(slide, col[0], { x: x + 24, y: 200, w: 230, h: 32, size: 23, bold: true, color: i === 0 ? C.green : i === 1 ? C.blue : C.amber });
    col[1].forEach((t, j) => bullet(slide, t, x + 30, 260 + j * 70, 270, i === 0 ? C.green : i === 1 ? C.blue : C.amber));
  });
  addShape(slide, { x: 108, y: 570, w: 1064, h: 62, fill: C.greenSoft, line: "#B9D8CB", lineWidth: 1 });
  addText(slide, "一番大事な運用ルール: 受講者配布用HTMLはそのまま配布し、講師の時刻変更は講師PCでの確認用途として使います。", { x: 132, y: 586, w: 1010, h: 30, size: 18, color: C.ink, bold: true });
  return slide;
}

const presentation = Presentation.create({ slideSize: { width: W, height: H } });
[slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8].forEach(fn => fn(presentation));

await fs.mkdir(PREVIEW_DIR, { recursive: true });
for (let i = 0; i < presentation.slides.count; i += 1) {
  const slide = presentation.slides.getItem(i);
  const blob = await presentation.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(PREVIEW_DIR, `slide-${String(i + 1).padStart(2, "0")}.png`), Buffer.from(await blob.arrayBuffer()));
}

const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(OUT);
console.log(OUT);
