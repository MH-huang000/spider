const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // 模擬正常瀏覽器行為
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
        'AppleWebKit/537.36 (KHTML, like Gecko) ' +
        'Chrome/133.0.0.0 Safari/537.36');
    
    await page.goto('https://www.dcard.tw/f/relationship', { waitUntil: 'networkidle2' });

    // 獲取文章 JSON
    const posts = await page.evaluate(() => {
        return fetch("https://www.dcard.tw/service/api/v2/forums/relationship/posts?popular=false&limit=30")
            .then(res => res.json());
    });

    // 保存 JSON 檔案
    fs.writeFileSync('dcard_relationship_posts.json', JSON.stringify(posts, null, 4));
    console.log("✅ 成功取得並保存資料！");

    await browser.close();
})();
