# Testing

## Validation

### Html Validation

Html validation was done with [https://validator.w3.org/](https://validator.w3.org/). All pages were tested by manually inputting the code into the validator.



#### **Home Page**

![Home Page](#)

#### **About Page**

![About Page](#)

#### **#Pages**

![Page](#)

#### **Error Pages**
![403 Error Page](#)
![404 Error Page](#)


### CSS Validation

The stylesheet was validated using [https://jigsaw.w3.org/css-validator/](https://jigsaw.w3.org/css-validator/)

![Stylesheet validation](#)


### Python Validation

Python code was validated using [http://pep8online.com/](http://pep8online.com/).  I also used the GitPod workspace to check for errors as I coded.  I found this useful as there were less errors once I ran the code through the validator.


### blogcc files

#### admin.py

![pep8 admin.py](#)

#### other.py

![pep8 other.py](#)


#### Gitpod Workspace

![Workspace](#)


## Lighthouse Testing

All pages were checked on lighthouse.  Results were over 90% for performance and best practice and 100% on Accessability and SEO on both mobile and desktop.  On the first test performance was very poor.  This was fixed by applying height and width to an image.


### **First Test**

![Lighthouse Poor Performance](#)

### **Final Test**

![Final Lighthouse Test](#)


## Manual Testing

To ensure that all elements of the website were working I carried out a detailed manual test and checked off the list as I went.

| Status | **Page Logged Out? Logged In?**
|:-------:|:--------|
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:
| &check; |:


## Bugs

### Bugs sub heading

Increase and Decrease Product Value

<details open>
<summary>Increase and Decrease Product Bug</summary>
<p align="center"><img src="https://res.cloudinary.com/rockymiss/image/upload/v1670880846/mcgraths/missing-bracket_wcp7od.png"></p>

Despite updating product_detail and quantity_input_script with the bug fix from Scott of Code Institute my products input value was not increasing or decreasing.  When clicking either the plus or minus icon the page would reload and just one item would add to the cart.  As I used bootstrap5 for this project a CDN link for js query fixed the page re-load.  The issue of the value increase or decrease remained and this was the result of a missing curly bracket as shown in the image above.  A simple fix yet a deadly needle in a haystack.  Thanks to tutor support for the help with this one.  
</details>

<details open>
<summary>Bug</summary>
<p align="center"><img src="#"></p>

</details>