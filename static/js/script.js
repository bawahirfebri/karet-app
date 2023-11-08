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

const itemsTitle = document.querySelectorAll('.menu-section .item .item-title')

itemsTitle.forEach(function(itemTitle) {
    itemTitle.addEventListener('click', function() {
        const list = itemTitle.parentElement.lastElementChild
        const arrow = itemTitle.lastElementChild
        
        if(list.id === 'hide') {
            list.setAttribute('id', '')
            arrow.firstElementChild.setAttribute('id', 'hide')
            arrow.lastElementChild.setAttribute('id', '')
        } else if(list.id === '') {
            list.setAttribute('id', 'hide')
            arrow.firstElementChild.setAttribute('id', '')
            arrow.lastElementChild.setAttribute('id', 'hide')
        }
    })
})

const layers = document.querySelectorAll('.layers .item-title')
const images = document.querySelectorAll('.img-canvas');

layers.forEach(function(layer) {
    layer.addEventListener('click', function() {
        const visibility = layer.lastElementChild.firstElementChild
        const visibilityOff = layer.lastElementChild.lastElementChild

        const index = images.length - Array.from(layers).indexOf(layer) - 1

        if(visibility.id === '') {
            visibility.setAttribute('id', 'hide')
            visibilityOff.setAttribute('id', '')
            images[index].style.display = 'none'
        } else if (visibility.id === 'hide') {
            visibility.setAttribute('id', '')
            visibilityOff.setAttribute('id', 'hide')
            images[index].style.display = 'block'
        }
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

    if(images.length == 1 && item.textContent === 'Segmentasi') {
        item.setAttribute('id', 'active')
    }

    if(images.length == 5 && (item.textContent === 'Segmentasi' || item.textContent === 'Tingkat Keparahan' || item.textContent === 'Download Gulma' || item.textContent === 'Download Karet')) {
        item.setAttribute('id', 'active')
    }

    item.addEventListener('click', function() {
        if(item.textContent === 'Layers') {
            fetch('/progress')
        }
    })
})

const filesInput = document.querySelectorAll('.file-input.citra')

filesInput.forEach(function(fileInput) {
    fileInput.addEventListener('change', function() {

        const submit = fileInput.parentElement.lastElementChild
        submit.click()
    })
})