version: '3'

services:
    web:
        build: .
        ports:
            - '80:80'
    db:
        image: redis:latest
        volumes:
            - ./:/data
