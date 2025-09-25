import { pgTable, serial, text, varchar, timestamp, boolean, integer, doublePrecision } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const tradingAccounts = pgTable('trading_accounts', {
  id: serial('id').primaryKey(),
  userId: integer('user_id').references(() => users.id),
  broker: text('broker').notNull(),
  accountNumber: text('account_number').notNull(),
  balance: doublePrecision('balance').default(0).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const positions = pgTable('positions', {
  id: serial('id').primaryKey(),
  accountId: integer('account_id').references(() => tradingAccounts.id),
  symbol: varchar('symbol', { length: 256 }).notNull(),
  status: text('status').notNull(),
  openTime: timestamp('open_time').defaultNow().notNull(),
});

export const notifications = pgTable('notifications', {
  id: serial('id').primaryKey(),
  userId: integer('user_id').references(() => users.id),
  message: text('message').notNull(),
  read: boolean('read').default(false).notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
});

export const educationalResources = pgTable('educational_resources', {
    id: serial('id').primaryKey(),
    title: text('title').notNull(),
    description: text('description').notNull(),
    skillLevel: text('skill_level').notNull(),
    category: text('category').notNull(),
    createdAt: timestamp('created_at').defaultNow().notNull(),
});