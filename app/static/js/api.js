var api = {}

var log = function() {
  console.log(arguments)
}


api.ajax = function(url, method, form, callback) {

  var request = {
    url: url,
    type: method,
    data: form,
    success: function(response){
        var r = JSON.parse(response)
        callback(r)
    },
    error: function(err){
      log('网络错误', err)
      var r = {
        'success': false,
        message: '网络错误'
      }
      callback(r)
    }
  }
  $.ajax(request)
}


api.get = function(url, response) {
    api.ajax(url, 'get', {}, response)
}


api.post = function(url, form, response) {
    api.ajax(url, 'post', form, response)
}

// ====================
// 以上是内部函数，内部使用
// --------------------
// 以下是功能函数，外部使用
// ====================

// 用户 API

api.userRegister = function(form, response) {
    var url = '/api/user/register'
    log("sss")
    api.post(url, form, response)
}


api.userLogin = function(form, response) {
    var url = '/api/user/login'
    log("sss")
    api.post(url, form, response)
}


api.userEdit = function(form, response) {
    var url = '/api/user/edit'
    log("sss")
    api.post(url, form, response)
}

// 单词 API

api.wordbookChoice = function(form, response) {
    var url = '/api/wordbook/choice'
    log("sss")
    api.post(url, form, response)
}


api.wordbookAdd = function(form, response) {
    var url = '/api/wordbook/add'
    log("sss")
    api.post(url, form, response)
}


api.wordsStartLearn = function(response) {
    var url = '/api/words/start_learn'
    log("sss")
    api.get(url, response)
}


api.wordsKnown = function(form, response) {
    var url = '/api/words/known'
    log("sss")
    api.post(url, form, response)
}


api.wordsUnknown = function(form, response) {
    var url = '/api/words/unknown'
    log("sss")
    api.post(url, form, response)
}


api.wordsDetail = function(response) {
    var url = '/api/words/detail'
    log("sss")
    api.get(url, response)
}


api.noteAdd = function(form, response) {
    var url = '/api/note/add'
    log("sss")
    api.post(url, form, response)
}


api.wordSetting = function(form, response) {
    var url = '/api/word/setting'
    log("sss")
    api.post(url, form, response)
}

