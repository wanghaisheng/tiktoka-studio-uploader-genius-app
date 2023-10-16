class logger {
  static consoleRaw = console
  static log(message) {
    message = `[ LOG ] ${message}`
    this.consoleRaw.log(message)
  }

  static error(message) {
    message = `[ ERROR ] ${message}`
    this.consoleRaw.log(message)
  }
}
const scriptVersion = '1.1.1'
logger.log(`##### Network IP v${scriptVersion}`)
let mainURL = 'https://whoer.net/v2/geoip2-'
const requestHeader = {
  'Accept-Language': 'zh',
}
let ipInfo = ''
let locationInfo = ''
let ispInfo = ''
function getLocationInfo() {
  return new Promise((resolve, reject) => {
    const cityOptions = {
      url: mainURL + 'city',
      headers: requestHeader,
    }
    $httpClient.get(cityOptions, function (error, response, data) {
      if (data) {
        let jsonData = JSON.parse(data)
        let country = jsonData.country_code
        let emoji = getFlagEmoji(jsonData.country_code)
        let city = jsonData.city_name || '未知'
        let ip = jsonData.network
        // 生成显示基础内容
        ipInfo = `IP 信息：${ip}`
        locationInfo = `所在地：${emoji}${country} - ${city}`
        resolve()
      }
    })
  })
}
function getISPInfo() {
  return new Promise((resolve, reject) => {
    const ispOptions = {
      url: mainURL + 'isp',
      headers: requestHeader,
    }
    $httpClient.get(ispOptions, function (error, response, data) {
      if (data) {
        let jsonData = JSON.parse(data)
        const isp = jsonData.isp
        ispInfo = `运营商：${isp}`
        resolve()
      }
    })
  })
}
function getNetworkInfo() {
  Promise.all([getLocationInfo(), getISPInfo()]).then(() => {
    const arguments = getArgument()
    logger.log(
      `✅ Script HTTP Request Success

       ###########################
       # Your ${arguments.moduleTitle}
       # ${ipInfo.substring(0, 2) + ipInfo.substring(3, ipInfo.length)}
       # ${locationInfo}
       # ${ispInfo}
       ###########################
      `
    )
    const body = {
      title: arguments.moduleTitle,
      content: `${ipInfo}\n${locationInfo}\n${ispInfo}`,
      icon: 'globe.asia.australia.fill',
    }
    $done(body)
  })
}

/**
 * 主要逻辑，程序入口
 */
;(() => {
  const scriptTimeout = 10000 - 500 // Surge 的网络请求超时为 10s
  setTimeout(() => {
    logger.error('⚠️ Script HTTP Request Timeout')
    $done({
      title: 'Proxy Network',
      content: '检测超时！请检查网络！或对 whoer.net 设置代理！',
      icon: 'globe.asia.australia.fill',
      'icon-color': '#e46c75',
    })
  }, scriptTimeout)

  // 获取网络信息
  logger.log('🎉 Script Start')
  getNetworkInfo()
})()

// Tool
function getFlagEmoji(countryCode) {
  if (countryCode.toUpperCase() == 'TW') {
    countryCode = 'CN'
  }
  const codePoints = countryCode
    .toUpperCase()
    .split('')
    .map(char => 127397 + char.charCodeAt())
  return String.fromCodePoint(...codePoints)
}

function getArgument() {
  return Object.fromEntries(
    $argument
      .split('&')
      .map(item => item.split('='))
      .map(([key, value]) => [key, decodeURIComponent(value)])
  )
}
