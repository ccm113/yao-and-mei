import { reactive, watch } from 'vue'

interface Photo {
  id: string
  url: string
}

interface WishItem {
  id: string
  destination: string
  description: string
  coordinates: { lat: number; lng: number }
}

const STORAGE_KEYS = {
  PHOTOS: 'shared_photos',
  WISHLIST: 'shared_wishlist'
}

const defaultPhotos: Photo[] = [
  { id: '1', url: 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=200' },
  { id: '2', url: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200' },
  { id: '3', url: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=200' },
  { id: '4', url: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200' },
  { id: '5', url: 'https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=200' }
]

const defaultWishlist: WishItem[] = [
  { id: '1', destination: '巴黎', description: '浪漫之都，埃菲尔铁塔', coordinates: { lat: 48.8566, lng: 2.3522 } },
  { id: '2', destination: '东京', description: '繁华都市，樱花季', coordinates: { lat: 35.6762, lng: 139.6503 } }
]

function loadData<T>(key: string, defaultValue: T): T {
  try {
    const saved = localStorage.getItem(key)
    return saved ? JSON.parse(saved) : defaultValue
  } catch {
    return defaultValue
  }
}

function saveData<T>(key: string, value: T): void {
  localStorage.setItem(key, JSON.stringify(value))
}

export const sharedStore = reactive({
  photos: loadData<Photo[]>(STORAGE_KEYS.PHOTOS, defaultPhotos),
  wishlist: loadData<WishItem[]>(STORAGE_KEYS.WISHLIST, defaultWishlist)
})

watch(
  () => sharedStore.photos,
  (newVal) => {
    saveData(STORAGE_KEYS.PHOTOS, newVal)
  },
  { deep: true }
)

watch(
  () => sharedStore.wishlist,
  (newVal) => {
    saveData(STORAGE_KEYS.WISHLIST, newVal)
  },
  { deep: true }
)

export function syncFromStorage(): void {
  sharedStore.photos = loadData<Photo[]>(STORAGE_KEYS.PHOTOS, defaultPhotos)
  sharedStore.wishlist = loadData<WishItem[]>(STORAGE_KEYS.WISHLIST, defaultWishlist)
}

export function setupStorageListener(callback?: () => void): void {
  window.addEventListener('storage', (event) => {
    if (event.key === STORAGE_KEYS.PHOTOS || event.key === STORAGE_KEYS.WISHLIST) {
      syncFromStorage()
      if (callback) callback()
    }
  })
}

export function addPhoto(url: string): void {
  const newPhoto: Photo = {
    id: Date.now().toString(),
    url
  }
  sharedStore.photos.push(newPhoto)
}

export function removePhoto(id: string): void {
  const index = sharedStore.photos.findIndex(p => p.id === id)
  if (index !== -1) {
    sharedStore.photos.splice(index, 1)
  }
}

export function updatePhoto(id: string, url: string): void {
  const photo = sharedStore.photos.find(p => p.id === id)
  if (photo) {
    photo.url = url
  }
}

export function addWishItem(destination: string, description: string, coordinates: { lat: number; lng: number }): void {
  const newItem: WishItem = {
    id: Date.now().toString(),
    destination,
    description,
    coordinates
  }
  sharedStore.wishlist.push(newItem)
}

export function removeWishItem(id: string): void {
  const index = sharedStore.wishlist.findIndex(w => w.id === id)
  if (index !== -1) {
    sharedStore.wishlist.splice(index, 1)
  }
}
