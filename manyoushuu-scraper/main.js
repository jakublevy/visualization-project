const puppeteer = require('puppeteer')
const { Scraper } = require('./scraper');

(async () => {
    await main()
})()

async function main() {
    const browser = await startPuppeteer()
    const page = (await browser.pages())[0]
    const scraper = new Scraper(browser, page)
    await scraper.scrapeAll()
    console.log('done')
}

async function startPuppeteer() {
    const options = { headless: false, ignoreHTTPSErrors: true, defaultViewport: null }
    return puppeteer.launch(options)
}