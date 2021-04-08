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

export interface Reaction {
    id: string,
    text: string,
}

export type Reactions = Record<'PHI'|'PLI'|'NLI'|'NHI', Reaction[]>;

export interface PendingFriend {
    status: 'Pending'|'Accepted',
    creator: number;
    friend: number;
}

export interface PendingFriendRequest extends PendingFriend {
    user?: User;
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

    static async getFriends($axios: NuxtAxiosInstance): Promise<any> {
        try {
            return await $axios.$get('/api/v1/friends/');
        } catch (e) {
            throw e;
        }
    }

    static async getFriend($axios: NuxtAxiosInstance, friend: number): Promise<any> {
        try {
            const friends = await this.getFriends($axios);
            //@ts-ignore
            return friends.find(f => f.friend === friend);
        } catch (e) {
            throw e;
        }
    }

    static async getPending($axios: NuxtAxiosInstance): Promise<PendingFriend[]>{
        try {
            const friends: any[] = await $axios.$get('/api/v1/friends/pending/');
            const pending: PendingFriend[] = friends.map(val => {
                return {
                    status: (val.status === 1 ? 'Pending' : 'Accepted'),
                    creator: val.creator,
                    friend: val.friend
                };
            });

            return pending;
        } catch (e) {
            throw e;
        }
    }

    static async getMyPending($axios: NuxtAxiosInstance, me: number): Promise<PendingFriendRequest[]>{
        try {
            let pending: PendingFriendRequest[] = await this.getPending($axios);
            pending = pending.filter(p => p.creator !== me);

            for (let friend of pending) {
                friend.user = await this.getProfile($axios, friend.creator.toString());
            }

            return pending;
        } catch (e) {
            throw e;
        }
    }

    static async getPendingFriend($axios: NuxtAxiosInstance, friend: number): Promise<'Pending'|'Accepted'|null> {
        try {
            const pending = await this.getPending($axios);
            const pendingFriend = pending.find(p => p.friend === friend);
            if (!pendingFriend) {
                return null;
            }

            return pendingFriend.status;
        } catch (e) {
            throw e;
        }
    }

    static async acceptFriend($axios: NuxtAxiosInstance, friend: number): Promise<PendingFriend> {
        try {
            const res = await $axios.$post('/api/v1/friends/pending/', {
                friend
            });

            return {
                creator: res.creator,
                friend: res.friend,
                status: res.status === 1 ? 'Pending' : 'Accepted'
            }
        } catch (e) {
            throw e;
        }
    }

    static async newFriend($axios: NuxtAxiosInstance, friend: number): Promise<PendingFriend> {
        try {
            const res = await $axios.$post('/api/v1/friends/', {
                friend
            });

            return {
                creator: res.creator,
                friend: res.friend,
                status: res.status === 1 ? 'Pending' : 'Accepted'
            }
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

    static async getMe($axios: NuxtAxiosInstance): Promise<User> {
        try {
            const res = await $axios.$get(`/api/v1/me/`);
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

    static async getReactionOptions($axios: NuxtAxiosInstance, categoryId: number): Promise<Reactions> {
        try {
            const reactions: Reactions = await $axios.$get(`/api/v1/categories/${categoryId}/`);
            const keys = Object.keys(reactions) as ('PHI'|'PLI'|'NLI'|'NHI')[];
            for (let key of keys) {
                reactions[key] = reactions[key].slice(0, 3);
            }

            return reactions;
        } catch (e) {
            throw e;
        }
    }

    static async newReaction($axios: NuxtAxiosInstance, video: number, emoji: string, reaction: string, timestamp: string) {
        try {
            await $axios.$post(`/api/v1/reactions/${video}/`, {
                emoji,
                text: reaction,
                timestamp
            });
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