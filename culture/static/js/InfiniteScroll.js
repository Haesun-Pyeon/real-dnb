class InfiniteScroll {
    constructor(path, wrapperId, rastPage) {
        if (path === undefined || wrapperId === undefined) throw Error('no parameter.');
        this.path = path;
        this.pNum = 2;
        this.wrapperId = wrapperId;
        this.rastPage = rastPage;
        this.enable = true;

        this.detectScroll();
    }

    detectScroll() {
        window.onscroll = (ev) => {
            var scrollHeight = $(window).scrollTop() + $(window).height();
            var documentHeight = $(document).height();

            if (scrollHeight + 300 >= documentHeight) this.getNewPost();
        };
    }
    getNewPost() {
        if (this.enable === false) return false;
        this.enable = false;
        const xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = () => {
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                if (xmlhttp.status == 200) {
                    this.pNum++;
                    const childItems = this.getChildItemsByAjaxHTML(xmlhttp.responseText);
                    this.appendNewItems(childItems);
                }
                return this.enable = true;
            }
        }
        xmlhttp.open("GET", `${location.href + this.path + this.pNum}`, true);
        xmlhttp.send();
    }

    getChildItemsByAjaxHTML(HTMLText) {
        const newHTML = document.createElement('html');
        newHTML.innerHTML = HTMLText;
        const childItems = newHTML.querySelectorAll(`#${this.wrapperId} > *`);
        return childItems;
    }

    appendNewItems(items) {
        let id = 0;
        items.forEach(item => {
            document.getElementById(this.wrapperId).appendChild(item);
            if (item.getAttribute('onclick')) {
                id = item.getAttribute('id');
                document.getElementById(id).click();
            }
        });
    }
}