export function isEmailValid(email: string): boolean {
  const pattern = /^[\w\.-]+@[\w\.-]+\.\w+$/;
  return pattern.test(email);
}

export function isPhoneValid(phone: string): boolean {
  const pattern = /^\+?[1-9]\d{1,14}$/;
  return pattern.test(phone);
}

export function isWebsiteValid(url: string): boolean {
  const pattern = /^https?:\/\/[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}.*$/;
  return pattern.test(url);
}
