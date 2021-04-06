import { NuxtAxiosInstance } from "@nuxtjs/axios";

export interface Category {
    id: number;
    title: string;
}

export interface User {
    id: number,
    username: string,
}

export interface Sources {
    src: string,
    type: 'video/mp4',
}

export interface Video {
    id: number,
    title: string,
    category: number,
    user: User
    date_uploaded: string,
    file: string,
    sources?: Sources[],
}

export default class Api {
    static async signup($axios: NuxtAxiosInstance, email: string, username: string, password: string) {
        try {
            await $axios.$post('/api/v1/register/', {
                email,
                username,
                password
            });
        } catch (e) {
            throw e;
        }
    }

    static async upload($axios: NuxtAxiosInstance) {
        try {
            await $axios.$post('/api/v1/videos/upload/');
        } catch (e) {
            throw e;
        }
    }

    static async getViralVideos($axios: NuxtAxiosInstance): Promise<Video[]> {
        try {
            return await $axios.$get('/api/v1/videos/viral/');
        } catch (e) {
            throw e;
        }
    }

    static async getVideoDetail($axios: NuxtAxiosInstance, videoId: string): Promise<Video> {
        try {
            return await $axios.$get(`/api/v1/videos/${videoId}`);
        } catch (e) {
            throw e;
        }
    }

    static async getProfile($axios: NuxtAxiosInstance, userId: string): Promise<User> {
        try {
            const res = await $axios.$get(`/api/v1/people/${userId}`);
            return res.user;
        } catch (e) {
            throw e;
        }
    }

    static async getCategories($axios: NuxtAxiosInstance): Promise<Category[]> {
        try {
            return await $axios.$get('/api/v1/categories/');
        } catch (e) {
            throw e;
        }
    }

    static async newPost($axios: NuxtAxiosInstance, title: string, category: number, file: File) {
        const form = new FormData();
        form.append('file', file);
        form.append('title', title);
        form.append('category', category.toString());

        try {
            await $axios.post('/api/v1/videos/upload/', form, {
                headers: {
                'Content-Type': 'multipart/form-data'
                }
            });
        } catch (e) {
            throw e;
        }
    }
}