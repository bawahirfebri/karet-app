window.addEventListener('load', function() {
    const progress = document.querySelector('.progress')
    const progressBar = document.querySelector('.progress-bar')

    const socket = io()
    socket.connect('http://127.0.0.1:3000/')
    socket.on('connect', function() {
        console.log('Connected!')
    })
    socket.on('update progress', function(percent) {
        console.log('Got percent: ' + percent)
        progress.style.width = '15rem'
        progressBar.style.width = percent + '%'
    })
})


const userImage = document.querySelector('.user-image')
const dropdown = document.querySelector('.dropdown')

userImage.addEventListener('click', function() {
    dropdown.id = (dropdown.id === 'hide') ? '' : 'hide'
})

const itemsTitle = document.querySelectorAll('.menu-section .item .item-title')

itemsTitle.forEach(function(itemTitle) {
    itemTitle.addEventListener('click', function() {
        const list = itemTitle.parentElement.lastElementChild
        const arrow = itemTitle.lastElementChild
        
        list.id = (list.id === 'hide') ? '' : 'hide'
        arrow.firstElementChild.id = (list.id === 'hide') ? '' : 'hide'
        arrow.lastElementChild.id = (list.id === 'hide') ? 'hide' : ''
    })
})


const layers = document.querySelectorAll('.layers .item-title')
const images = document.querySelectorAll('.img-canvas');

layers.forEach(function(layer) {
    layer.addEventListener('click', function() {
        const visibility = layer.lastElementChild.firstElementChild
        const visibilityOff = layer.lastElementChild.lastElementChild

        const index = images.length - Array.from(layers).indexOf(layer) - 1

        visibility.id = (visibility.id === '') ? 'hide' : '';
        visibilityOff.id = (visibility.id === 'hide') ? '' : 'hide';
        images[index].style.display = (visibility.id === 'hide') ? 'none' : 'block';
    })
})

const itemsInput = document.querySelectorAll('.input .small-text')

itemsInput.forEach(function(itemInput) {
    itemInput.addEventListener('click', function() {
        itemInput.parentElement.lastElementChild.firstElementChild.click()
    })

    if(images.length == 1 && itemInput.textContent === 'Input Data Occurance') {
        itemInput.setAttribute('id', 'active')
    }
})

const items = document.querySelectorAll('.small-text')

items.forEach(function(item) {

    if(images.length == 1 && (item.textContent === 'Segmentasi' || item.textContent === 'Layers' || item.textContent === 'Data Occurance')) {
        item.setAttribute('id', 'active')
    }

    if(images.length == 5 && (item.textContent === 'Segmentasi' || item.textContent === 'Tingkat Keparahan' || item.textContent === 'Download Gulma' || item.textContent === 'Download Karet' || item.textContent === 'Layers' || item.textContent === 'Data Occurance')) {
        item.setAttribute('id', 'active')
    }
})

const filesInput = document.querySelectorAll('.file-input.citra')

filesInput.forEach(function(fileInput) {
    fileInput.addEventListener('change', function() {

        const submit = fileInput.parentElement.lastElementChild
        submit.click()
    })
})

const layersButton = document.querySelector('.small-text[data-layers]');
const layersSection = document.querySelector('.control-section .layers');

const dataOccuranceButton = document.querySelector('.small-text[data-occurance]');
const occuranceInputSection = document.querySelector('.control-section .item-input');
const occuranceListSection = document.querySelector('.control-section .item-list');

const layersStatus = localStorage.getItem('layersStatus');
const occuranceInputStatus = localStorage.getItem('occuranceInputStatus');
const occuranceListStatus = localStorage.getItem('occuranceListStatus');

layersSection.id = layersStatus === null ? 'hide' : layersStatus;
occuranceInputSection.id = occuranceInputStatus === null ? 'hide' : occuranceInputStatus;
occuranceListSection.id = occuranceListStatus === null ? 'hide' : occuranceListStatus;

dataOccuranceButton.addEventListener('click', toggleSections);
layersButton.addEventListener('click', toggleSections);

function toggleSections() {

    localStorage.setItem('layersStatus', layersButton === this ? '' : 'hide');
    localStorage.setItem('occuranceInputStatus', dataOccuranceButton === this ? '' : 'hide');
    localStorage.setItem('occuranceListStatus', dataOccuranceButton === this ? '' : 'hide');

    layersSection.id = layersButton === this ? '' : 'hide';
    occuranceInputSection.id = dataOccuranceButton === this ? '' : 'hide';
    occuranceListSection.id = dataOccuranceButton === this ? '' : 'hide';
}

