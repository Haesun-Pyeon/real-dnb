var path = document.location.pathname;

if (path.includes('bookmap')) {
    result = 'MAP'
} else if (path.includes('themamap')) {
    result = 'THEME MAP'
} else if (path.includes('board')) {
    result = 'CULTURE PROGRAMS'
} else if (path.includes('mypage')) {
    result = 'MY PAGE'
} else if (path.includes('signup')) {
    result = '회원가입'
} else if (path.includes('login')) {
    result = '로그인'
} else if (path.includes('storedetail')) {
    result = 'INFORMATION'
} else if (path.includes('ranking')) {
    result = 'RANKING'
}
else {
    result = '동네북'
}

document.write(result)
