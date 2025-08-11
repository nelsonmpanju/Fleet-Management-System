// Material for MkDocs Official Site Style - Repository Info
document.addEventListener('DOMContentLoaded', function() {
    // Inject GitHub repository info into the header like Material for MkDocs
    const repoSource = document.querySelector('.md-header__source');
    if (repoSource) {
        const repoUrl = repoSource.querySelector('a').href;
        const repoPath = repoUrl.split('github.com/')[1]; // e.g., nelsonmpanju/Fleet-Management-System

        if (repoPath) {
            // Create container for repo info
            const repoInfo = document.createElement('div');
            repoInfo.style.display = 'flex';
            repoInfo.style.alignItems = 'center';
            repoInfo.style.gap = '0.5rem';
            repoInfo.style.fontSize = '0.75rem';
            repoInfo.style.color = 'rgba(255, 255, 255, 0.9)';
            repoInfo.style.marginLeft = '1rem';

            // Add version info (like Material for MkDocs shows "9.6.16")
            const version = document.createElement('span');
            version.textContent = 'v1.0.0';
            version.style.fontWeight = '500';
            repoInfo.appendChild(version);

            // Add separator
            const separator = document.createElement('span');
            separator.textContent = '•';
            separator.style.opacity = '0.6';
            repoInfo.appendChild(separator);

            // Add stars badge
            const starsBadge = document.createElement('img');
            starsBadge.src = `https://img.shields.io/github/stars/${repoPath}?style=flat-square&label=Stars&color=denimblue&labelColor=rgba(255,255,255,0.1)`;
            starsBadge.alt = 'GitHub Stars';
            starsBadge.style.height = '16px';
            starsBadge.style.verticalAlign = 'middle';
            repoInfo.appendChild(starsBadge);

            // Add forks badge
            const forksBadge = document.createElement('img');
            forksBadge.src = `https://img.shields.io/github/forks/${repoPath}?style=flat-square&label=Forks&color=denimblue&labelColor=rgba(255,255,255,0.1)`;
            forksBadge.alt = 'GitHub Forks';
            forksBadge.style.height = '16px';
            forksBadge.style.verticalAlign = 'middle';
            repoInfo.appendChild(forksBadge);

            // Insert after the existing repo link
            repoSource.appendChild(repoInfo);
        }
    }

    // Add smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy button functionality for code blocks
    document.querySelectorAll('pre code').forEach(block => {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>';
        button.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: rgba(255, 255, 255, 0.1);
            border: none;
            border-radius: 0.2rem;
            color: rgba(255, 255, 255, 0.7);
            cursor: pointer;
            padding: 0.25rem;
            opacity: 0;
            transition: opacity 0.2s;
        `;

        const pre = block.parentElement;
        pre.style.position = 'relative';
        pre.appendChild(button);

        pre.addEventListener('mouseenter', () => {
            button.style.opacity = '1';
        });

        pre.addEventListener('mouseleave', () => {
            button.style.opacity = '0';
        });

        button.addEventListener('click', () => {
            navigator.clipboard.writeText(block.textContent).then(() => {
                button.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20,6 9,17 4,12"></polyline></svg>';
                setTimeout(() => {
                    button.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>';
                }, 2000);
            });
        });
    });
});