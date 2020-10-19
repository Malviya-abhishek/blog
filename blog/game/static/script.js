
// file:///d:/codesublime/js/New%20folder/


const canvas = document.querySelector('canvas')
const scoreEl = document.querySelector('#scoreEl')
const weponEl = document.querySelector('#weponEl')
const startGameBtn = document.querySelector('#startGameBtn')
const modelEl = document.querySelector('#modelEl')
const bigScoreEL = document.querySelector('#bigScoreEL')
const difficulty = 1
const ctx = canvas.getContext('2d')
const enemyVelocity = 1
const projectileVelocity = 4
const particleVelocity = 6
const playerVelocity = 2
const width = canvas.width
const height = canvas.height
let playerVelocities = { "x": 0, "y": 0 }
let asd = 123




canvas.width = window.innerWidth // does not need window but just for satisfaction
canvas.height = window.innerHeight


class Player {
    constructor(x, y, radius, color, velocity) {
        this.x = x
        this.y = y
        this.radius = radius
        this.color = color
        this.velocity = velocity
    }

    draw() {
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false)
        ctx.fillStyle = this.color
        ctx.fill()
    }
    update() {
        this.draw()
        this.x += this.velocity * playerVelocities.x
        this.y += this.velocity * playerVelocities.y
    }
}

class Projectile {
    constructor(x, y, radius, color, velocity) {
        this.x = x
        this.y = y
        this.radius = radius
        this.color = color
        this.velocity = velocity
    }
    draw() {
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false)
        ctx.fillStyle = this.color
        ctx.fill()
    }

    update() {
        this.draw()
        this.x = this.x + this.velocity.x
        this.y = this.y + this.velocity.y
    }

}

class Enemy {
    constructor(x, y, radius, color, velocity) {
        this.x = x
        this.y = y
        this.radius = radius
        this.color = color
        this.velocity = velocity
    }
    draw() {
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false)
        ctx.fillStyle = this.color
        ctx.fill()
    }

    update() {
        this.draw()
        this.x = this.x + this.velocity.x
        this.y = this.y + this.velocity.y
    }

}

class Enemy2 {
    constructor(x, y, radius, color, velocity, double) {
        this.xCenter = x
        this.yCenter = y
        this.x = null
        this.y = null
        this.radius = radius
        this.Radius = 2 * this.radius
        this.color = color
        this.velocity = velocity
        this.val = 0
        this.double = double
    }
    draw() {
        this.val++
        let angle = this.val * .05 + this.double * Math.PI
        this.x = this.xCenter + this.Radius * Math.cos(angle)
        this.y = this.yCenter + this.Radius * Math.sin(angle)
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false)
        ctx.fillStyle = this.color
        ctx.fill()
    }
    update() {
        this.draw()
        this.xCenter += this.velocity.x
        this.yCenter += this.velocity.y
    }
}

class Enemy3 {
    constructor(x, y, radius, color, velocity, double) {
        this.xCenter = x
        this.yCenter = y
        this.x = null
        this.y = null
        this.radius = radius
        this.Amplitude = 2 * this.radius
        this.color = color
        this.velocity = velocity
        this.val = 0
        this.double = double
    }

    draw() {

        this.val++

        let perAngle = this.angle + Math.PI / 2

        let ang = this.val * .05
        let Amp = this.Amplitude * Math.sin(ang)

        this.x = this.xCenter + Amp * this.velocity.y
        this.y = this.yCenter + Amp * this.velocity.x * -1

        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false)
        ctx.fillStyle = this.color
        ctx.fill()

    }

    update() {
        this.draw()
        this.xCenter += this.velocity.x
        this.yCenter += this.velocity.y
    }
}

const friction = 0.95

class Particle {
    constructor(x, y, radius, color, velocity) {
        this.x = x
        this.y = y
        this.radius = radius
        this.color = color
        this.velocity = velocity
        this.alpha = 1
    }
    draw() {
        ctx.save()
        ctx.globalAlpha = this.alpha
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false)
        ctx.fillStyle = this.color
        ctx.fill()
        ctx.restore()
    }

    update() {
        this.draw()
        this.velocity.x *= friction
        this.velocity.y *= friction
        this.x = this.x + this.velocity.x
        this.y = this.y + this.velocity.y
        this.alpha -= 0.01
    }

}


const player = new Player(canvas.width / 2, canvas.height / 2, 10, 'white', playerVelocity)
player.draw()

let projectiles = []
let enemies = []
let particles = []
let score = 0
let scoreLast = 0
let weponScore = 0

function init() {
    projectiles = []
    enemies = []
    particles = []
    score = 0
    weponScore = 0
    scoreEl.innerHTML = 0
    weponEl.innerHTML = 0
}

function animate() {
    let animationId = requestAnimationFrame(animate)

    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    particles.forEach((particle, index) => {
        if (particle.alpha <= 0)
            particles.splice(index, 1)
        else
            particle.update()
    });

    player.update()

    projectiles.forEach((projectile, projectileIndex) => {
        projectile.update()

        if (projectile.x - projectile.radius < 0 ||
            projectile.y - projectile.radius < 0 ||
            projectile.x + projectile.radius > canvas.width ||
            projectile.y + projectile.radius > canvas.height) {
            setTimeout(() => {
                projectiles.splice(projectileIndex, 1)
            }, 0);
        }
    });

    enemies.forEach((enemy, enemyIndex) => {

        let angle = Math.atan2(player.y - enemy.y, player.x - enemy.x)
        let velocity = {
            'x': Math.cos(angle) * enemyVelocity,
            'y': Math.sin(angle) * enemyVelocity
        }

        enemy.velocity = velocity

        enemy.update()

        const distance = Math.hypot(player.x - enemy.x, player.y - enemy.y)

        if (enemy.radius + player.radius > distance + 2) {
            cancelAnimationFrame(animationId)
            modelEl.style.display = 'flex'
            bigScoreEL.innerHTML = score

        }

        projectiles.forEach((projectile, projectileIndex) => {
            const distance = Math.hypot(projectile.x - enemy.x, projectile.y - enemy.y)
            if (enemy.radius + projectile.radius >= distance) {
                for (let i = 0; i < enemy.radius * 2; ++i) {
                    let velocity = { x: (Math.random() - 0.5) * particleVelocity, y: (Math.random() - 0.5) * particleVelocity }
                    let particle = new Particle(projectile.x, projectile.y, Math.random() * 2, enemy.color, velocity)
                    particles.push(particle)
                }

                if (enemy.radius > 20) {
                    score += 100
                    scoreEl.innerHTML = score
                    gsap.to(enemy, {
                        radius: enemy.radius - 10
                    })
                    if (score && (score - scoreLast) / score > 0.5) {
                        scoreLast = score
                        weponScore++;
                        weponEl.innerHTML = weponScore
                    }
                    setTimeout(() => {
                        projectiles.splice(projectileIndex, 1)
                    }, 0);
                }
                else {
                    score += 250
                    if (score && (score - scoreLast) / score > 0.5) {
                        scoreLast = score
                        weponScore++;
                        weponEl.innerHTML = weponScore
                    }
                    scoreEl.innerHTML = score
                    setTimeout(() => {
                        enemies.splice(enemyIndex, 1)
                        projectiles.splice(projectileIndex, 1)
                    }, 0);
                }

            }
        });
    });
}
// enemy
function spawnEnemies() {
    setInterval(() => {
        if (enemies.length - 1 > difficulty)
            return;

        const radius = (Math.random() * 30) + (10);
        let x
        let y
        if (Math.random() < .5) {
            y = Math.random() * canvas.height
            x = Math.random() < 0.5 ? canvas.width + radius : 0 - radius
        }
        else {
            x = Math.random() * canvas.width
            y = Math.random() < 0.5 ? canvas.height + radius : 0 - radius
        }
        const color = `hsl( ${Math.random() * 360} , 50%, 50%)`
        const angle = Math.atan2(player.y - y, player.x - x)
        const velocity = {
            'x': Math.cos(angle) * enemyVelocity,
            'y': Math.sin(angle) * enemyVelocity
        }
        let enemy
        let code = Math.random()

        if (code < .5)
            enemy = new Enemy(x, y, radius, color, velocity)
        else if (code < .7)
            enemy = new Enemy2(x, y, radius, color, velocity, false)
        else if (code < .9) {
            enemy = new Enemy2(x, y, radius, color, velocity, false)
            enemies.push(new Enemy2(x, y, radius, color, velocity, true))
        }
        else if (code < 1) {
            enemy = new Enemy3(x, y, radius, color, velocity, false)
        }

        enemies.push(enemy)
    }, 1000);
}


// input

window.addEventListener('click', (event) => {
    const angle = Math.atan2(event.clientY - player.y, event.clientX - player.x)
    let velocity = { 'x': Math.cos(angle) * projectileVelocity, 'y': Math.sin(angle) * projectileVelocity }
    projectiles.push(new Projectile(player.x, player.y, 5, 'white', velocity))
})

window.addEventListener('keypress', (event) => {
    let keyCode = event.key
    if (keyCode == 'w')
        playerVelocities.y = -1
    else if (keyCode == 'a')
        playerVelocities.x = -1
    else if (keyCode == 's')
        playerVelocities.y = 1
    else if (keyCode == 'd')
        playerVelocities.x = 1
    else if (weponScore > 0)
        weapons(keyCode)
})


window.addEventListener('keyup', (event) => {
    let keyCode = event.key
    if (keyCode == 'w' && playerVelocities.y == -1)
        playerVelocities.y = 0
    else if (keyCode == 'a' && playerVelocities.x == -1)
        playerVelocities.x = 0
    else if (keyCode == 's' && playerVelocities.y == 1)
        playerVelocities.y = 0
    else if (keyCode == 'd' && playerVelocities.x == 1)
        playerVelocities.x = 0
})


// start game
startGameBtn.addEventListener('click', () => {
    init()
    modelEl.style.display = 'none'
    animate()
    spawnEnemies()
})


// special weapons

function weapons(key) {
    weponScore--;
    weponEl.innerHTML = weponScore
    if (key == 1)
        stormTrooper()
    else if (key == 2)
        hailStorm()
    else if (key == 3)
        blossomCherry()
    else if (key == 4)
        hellRaiser()
    else if (key == 5)
        grenade()
}

function stormTrooper() {
    if (playerVelocities.y == 0 && playerVelocities.x == 0)
        return;
    let angleIn = Math.atan2(playerVelocities.y, playerVelocities.x)
    let partion = (Math.PI * 12) / 180
    for (let i = -2; i < 3; ++i) {
        let angle = angleIn + i * partion
        let velocity = { 'x': Math.cos(angle) * projectileVelocity, 'y': Math.sin(angle) * projectileVelocity }
        projectiles.push(new Projectile(player.x, player.y, 5, 'white', velocity))
    }
}

function hailStorm() {
    let n = 12
    for (let i = 0; i < n; ++i) {
        let angle = (i * Math.PI * 2) / n
        let velocity = { 'x': Math.cos(angle) * projectileVelocity, 'y': Math.sin(angle) * projectileVelocity }
        projectiles.push(new Projectile(player.x, player.y, 5, 'white', velocity))
    }
}

function blossomCherry() {
    let n = 8
    let projectileArr = []
    for (let i = 0; i < n; ++i) {
        let angle = (i * Math.PI * 2) / n
        let velocity = { 'x': Math.cos(angle) * projectileVelocity, 'y': Math.sin(angle) * projectileVelocity }
        projectile = new Projectile(player.x, player.y, 5, 'white', velocity)
        projectiles.push(projectile)
        projectileArr.push(projectile)
    }
    for (let projectile of projectileArr)
        setTimeout(blossomCherryHelper, 700, projectile);
}

function blossomCherryHelper(projectile) {
    let m = 4
    for (let j = 0; j < m; ++j) {
        let angle = (j * Math.PI * 2) / m + (Math.PI / 4)
        let velocity = { 'x': Math.cos(angle) * projectileVelocity, 'y': Math.sin(angle) * projectileVelocity }
        projectiles.push(new Projectile(projectile.x, projectile.y, 5, 'red', velocity))
    }
}

function hellRaiser() {
    let n = 16
    let x = player.x, y = player.y
    for (let i = 0; i < n * 2; ++i)
        setTimeout(hellRaiserHelper, (i * 1000) / n, i, n, x, y);
}

function hellRaiserHelper(i, n, x, y) {
    let angle = (i * Math.PI * 2) / n
    let velocity = { 'x': Math.cos(angle) * projectileVelocity, 'y': Math.sin(angle) * projectileVelocity }
    projectiles.push(new Projectile(x, y, 5, 'blue', velocity))

}

function grenade() {
    let radius = 20
    for (let i = 0; i < radius * 2; ++i) {
        let velocity = { x: (Math.random() - 0.5) * projectileVelocity, y: (Math.random() - 0.5) * projectileVelocity }
        let projectile = new Projectile(player.x + -100 * playerVelocities.x, player.y + -100 * playerVelocities.y, Math.random() * 2, 'red', velocity)
        projectiles.push(projectile)
    }
}