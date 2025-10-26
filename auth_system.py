#!/usr/bin/env python3
"""
Simple Authentication System for Alpaca Trading Bot
Basic session-based authentication with in-memory storage
"""
import hashlib
import secrets
import time
from typing import Dict, Optional

class SimpleAuth:
    def __init__(self):
        # Simple user database (in production, use proper database)
        self.users = {
            'admin': self._hash_password('trading123'),
            'trader': self._hash_password('alpaca2024'),
            'demo': self._hash_password('demo123')
        }
        
        # Session storage (in production, use Redis/database)
        self.sessions: Dict[str, dict] = {}
        
        # Session timeout (30 minutes)
        self.session_timeout = 30 * 60
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = "alpaca_trading_bot_salt"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials"""
        if username not in self.users:
            return False
        
        hashed_password = self._hash_password(password)
        return self.users[username] == hashed_password
    
    def create_session(self, username: str) -> str:
        """Create new session for authenticated user"""
        session_id = secrets.token_urlsafe(32)
        self.sessions[session_id] = {
            'username': username,
            'created_at': time.time(),
            'last_accessed': time.time()
        }
        return session_id
    
    def validate_session(self, session_id: Optional[str]) -> Optional[str]:
        """Validate session and return username if valid"""
        if not session_id or session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        current_time = time.time()
        
        # Check if session expired
        if current_time - session['last_accessed'] > self.session_timeout:
            del self.sessions[session_id]
            return None
        
        # Update last accessed time
        session['last_accessed'] = current_time
        return session['username']
    
    def logout(self, session_id: str) -> bool:
        """Remove session (logout)"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        current_time = time.time()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if current_time - session['last_accessed'] > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
    
    def get_session_info(self, session_id: str) -> Optional[dict]:
        """Get session information"""
        if session_id in self.sessions:
            return self.sessions[session_id].copy()
        return None

# Global auth instance
auth_system = SimpleAuth()