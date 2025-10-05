
import { db } from './db.js';
import { 
  users, 
  tradingAccounts, 
} from '../../database/schema.js';

async function seed() {
  console.log('🌱 Seeding database...');

  try {
    // Create demo user
    const [user] = await db.insert(users).values({
      email: 'demo@genztradingbot.com',
      username: 'demo_trader',
      passwordHash: 'demo_password_hash',
    }).returning();

    console.log('✅ Created demo user');

    // Create demo trading account
    await db.insert(tradingAccounts).values({
      userId: user.id,
      broker: 'bybit',
      accountNumber: 'demo_account_123',
      accountName: 'Demo Trading Account',
      balance: '10000.00',
      currency: 'USDT'
    });

    console.log('✅ Created demo trading account');
    console.log('🎉 Database seeding completed successfully!');

  } catch (error) {
    console.error('❌ Database seeding failed:', error);
    process.exit(1);
  }
}

seed();
