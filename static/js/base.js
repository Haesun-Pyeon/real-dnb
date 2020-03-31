var path = document.location.pathname;

if (path.includes('thema')) {
    result = 'THEME MAP'
} else if (path.includes('bookmap/store')) {
    result = 'INFORMATION'
} else if (path.includes('realmap') | path.includes('search')) {
    result = 'MAP'
} else if (path.includes('board')) {
    result = 'DAILY NEWS'
} else if (path.includes('mypage')) {
    result = 'MY PAGE'
} else if (path.includes('signup')) {
    result = '회원가입'
} else if (path.includes('login')) {
    result = '로그인'
} else if (path.includes('ranking')) {
    result = 'RANKING'
} else if (path.includes('chat')) {
    result = 'MESSAGE'
} else {
    result = '동네북'
}

document.write(result)
