<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
-->


<!-- PROJECT LOGO -->
<!--
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->
<h1 align="center">Swebay: An online e-bidding platform</h1>
<!--
  <p align="center">
    project_description
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>
-->


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#entity-relation-diagram">Entity-Relation Diagram</a></li>
        <li><a href="#technologies-used">Technologies Used</a></li>
        <li><a href="#software-requirements-specification-srs">Software Requirements Specification (SRS)</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#how-it-works">How it Works</a></li>
    <li><a href="#top-contributors">Top Contributors</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Swebay is an e-bidding platform designed to provide a secure, user-friendly, and efficient environment where users can engage in online auctions. The platform supports various types of transactions including item listings, bidding, purchases, and user ratings. The primary stakeholders of the system include general users, super users, and VIP users, each having distinct levels of access and capabilities within the platform. Additionally, the system ensures secure authentication, handles user suspensions based on performance, and offers exclusive privileges for VIP users.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Features
* User registration with validation to prevent bots from accessing the system.
* Item listings with prices and deadlines for bids.
* Bidding and transaction processing, with money transfers from buyers to sellers.
* A rating system where users evaluate each other after transactions, impacting user status.
* A VIP system that rewards users with premium privileges for positive engagement.
* A creative feature that includes exclusive events for VIPs, such as live bidding sessions.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Entity-Relation Diagram
![Flowchart](https://github.com/MChaudhry9/ecom-bidding-csc322/blob/master/project_images/swebay%20diagram.png) 
<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Technologies Used

* [![Django](https://img.shields.io/badge/Django-20232A?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
* [![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
* [![HTML](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
* [![CSS](https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
* [![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Software Requirements Specification (SRS)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.


### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/MChaudhry9/ecom-bidding-csc322.git
   ```
2. Install Dependencies
  ```sh
  pip install django pandas pillow
  ```
3. Set Up the Database
In your terminal paste the following commands:
  ```sh
  python manage.py makemigrations
  python manage.py migrate
  ```
4. Run the Development Server
  ```sh
  python manage.py runserver
  ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## How it Works
1. **Item Listing**  
   * Registered users can create detailed listings for items they wish to auction, specifying starting bids and auction durations.

2. **User Roles and Participation**  
   * **Visitors**: Browse items and apply for registration.  
   * **Registered Users**: Place bids, list items for auction, and participate in live auctions.  
   * **VIP Users**: Access live bidding sessions and exclusive features.  

3. **Auction Process**  
   * The system updates bid information in real time, ensuring all participants have the latest updates.  

4. **Transaction Completion**  
   * Once an auction ends, the winner is notified, and secure payment and item transfer processes are initiated.  
   * Ratings are exchanged, and complaints, if any, are managed by Super Users.  

5. **Platform Security**  
   * Includes authentication, bot prevention, and user management with a strike-based suspension system for bad behavior.  

6. **VIP Privileges**  
   * VIPs enjoy premium perks like live bidding and exclusive auctions.


<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- CONTRIBUTING -->

### Top contributors:

* Mamuna Chaudhry
* Brandon B
* Ratul Bin Rasul
* Kalelo Dukuray

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
