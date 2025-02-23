// 現在のページを識別
const currentPage = document.body.getAttribute('data-page');

// 処理をページごとに分ける
switch (currentPage) {
    // index.htmlの処理
    case 'index': {
        // レスポンシブHTMLをロードする関数
        function loadResponsiveHTML() {
            const iframe = document.getElementById('responsive-frame');

            if (!iframe) {
                console.error("ID 'responsive-frame' の iframe 要素が見つかりません。");
                return;
            }

            iframe.src = window.innerWidth > 768 ? "desktop.html" : "mobile.html";
        }

        // 初期ロードとウィンドウサイズ変更時に関数を実行
        window.addEventListener('load', loadResponsiveHTML);
        window.addEventListener('resize', loadResponsiveHTML);

        break;
    }

    // desktop.htmlの処理
    case 'desktop': {
        document.addEventListener('keydown', (event) => {
            if (event.ctrlKey && event.key === 'End') {
                event.preventDefault();
                const footer = document.getElementById('footer');
                if (footer) {
                    footer.scrollIntoView({ behavior: 'smooth' });
                }
            }

            if (event.ctrlKey && event.key === 'Home') {
                event.preventDefault();
                const fv = document.getElementById('fv');
                if (fv) {
                    fv.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });

        break;
    }

    // mobile.htmlの処理
    case 'mobile': {
        const menuSp = document.getElementById('menu-sp');
        const navSp = document.getElementById('nav-sp');
        const close = document.getElementById('close');
        const links = navSp.querySelectorAll('a');
        let isNavOpen = false;

        function toggleNav() {
            isNavOpen = !isNavOpen;
            navSp.style.display = isNavOpen ? 'block' : 'none';
        }

        function closeNav() {
            navSp.style.display = 'none';
            isNavOpen = false;
            menuSp.src = 'mobile_images/hamburger.png';
        }

        menuSp.addEventListener('click', toggleNav);

        links.forEach(link => {
            link.addEventListener('click', closeNav);
        });

        document.addEventListener('click', (event) => {
            if (!navSp.contains(event.target) && event.target !== menuSp) {
                closeNav();
            }
        });

        close.addEventListener('click', closeNav);

        break;
    }

    default:
        console.warn("不明なページタイプです");
        break;
}
