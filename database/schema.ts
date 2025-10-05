import {
  pgTable,
  serial,
  varchar,
  boolean,
  timestamp,
  integer,
  decimal,
  json,
  index,
} from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  username: varchar('username', { length: 50 }).notNull().unique(),
  email: varchar('email', { length: 100 }).notNull().unique(),
  passwordHash: varchar('password_hash', { length: 255 }).notNull(),
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});

export const tradingAccounts = pgTable('trading_accounts', {
  id: serial('id').primaryKey(),
  userId: integer('user_id').references(() => users.id),
  accountName: varchar('account_name', { length: 100 }).notNull(),
  broker: varchar('broker', { length: 50 }).notNull(),
  accountNumber: varchar('account_number', { length: 100 }),
  balance: decimal('balance', { precision: 15, scale: 2 }).default('0.00'),
  currency: varchar('currency', { length: 10 }).default('USD'),
  isActive: boolean('is_active').default(true),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});

export const tradingPairs = pgTable('trading_pairs', {
    id: serial('id').primaryKey(),
    symbol: varchar('symbol', { length: 20 }).notNull().unique(),
    baseCurrency: varchar('base_currency', { length: 10 }).notNull(),
    quoteCurrency: varchar('quote_currency', { length: 10 }).notNull(),
    isActive: boolean('is_active').default(true),
    createdAt: timestamp('created_at').defaultNow(),
});

export const marketData = pgTable('market_data', {
    id: serial('id').primaryKey(),
    symbol: varchar('symbol', { length: 20 }).notNull(),
    timestamp: timestamp('timestamp').notNull(),
    openPrice: decimal('open_price', { precision: 15, scale: 5 }),
    highPrice: decimal('high_price', { precision: 15, scale: 5 }),
    lowPrice: decimal('low_price', { precision: 15, scale: 5 }),
    closePrice: decimal('close_price', { precision: 15, scale: 5 }),
    volume: decimal('volume', { precision: 20, scale: 2 }),
    createdAt: timestamp('created_at').defaultNow(),
}, (table) => {
    return {
        marketDataSymbolTimestampIdx: index('market_data_idx_symbol_timestamp').on(table.symbol, table.timestamp),
    };
});

export const tradingSignals = pgTable('trading_signals', {
    id: serial('id').primaryKey(),
    symbol: varchar('symbol', { length: 20 }).notNull(),
    signalType: varchar('signal_type', { length: 20 }).notNull(),
    confidence: decimal('confidence', { precision: 5, scale: 2 }),
    price: decimal('price', { precision: 15, scale: 5 }),
    timestamp: timestamp('timestamp').notNull(),
    modelVersion: varchar('model_version', { length: 50 }),
    features: json('features'),
    createdAt: timestamp('created_at').defaultNow(),
}, (table) => {
    return {
        tradingSignalsSymbolTimestampIdx: index('trading_signals_idx_symbol_timestamp').on(table.symbol, table.timestamp),
    };
});

export const trades = pgTable('trades', {
    id: serial('id').primaryKey(),
    userId: integer('user_id').references(() => users.id),
    accountId: integer('account_id').references(() => tradingAccounts.id),
    symbol: varchar('symbol', { length: 20 }).notNull(),
    tradeType: varchar('trade_type', { length: 10 }).notNull(),
    quantity: decimal('quantity', { precision: 15, scale: 5 }).notNull(),
    price: decimal('price', { precision: 15, scale: 5 }).notNull(),
    totalAmount: decimal('total_amount', { precision: 15, scale: 2 }).notNull(),
    status: varchar('status', { length: 20 }).default('PENDING'),
    signalId: integer('signal_id').references(() => tradingSignals.id),
    createdAt: timestamp('created_at').defaultNow(),
    executedAt: timestamp('executed_at'),
});