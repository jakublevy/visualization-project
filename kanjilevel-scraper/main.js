const readline = require('readline')
const puppeteer = require('puppeteer');
const fs = require('fs');
const {KanjiLevelScraper} = require("./KanjiLevelScraper");

(async () => {
    await main()
})()

async function main() {
    const kanjiJson = fs.readFileSync('../data/kanji.json')
    const kanji = JSON.parse(kanjiJson)

    const browser = await startPuppeteer()
    const page = (await browser.pages())[0]
    const kanjiLevelScraper = new KanjiLevelScraper(browser, page, kanji)
    await kanjiLevelScraper.scrapeAll()
    console.log('done')
}

async function startPuppeteer() {
    const options = { headless: false, ignoreHTTPSErrors: true, defaultViewport: null}
    return puppeteer.launch(options)
}